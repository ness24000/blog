from typing import Tuple, List
import sqlite3
from logging import Logger

from dbutils.pooled_db import PooledDB


class DBHandler:
    def __init__(
        self,
        path_to_db: str,
        logger: Logger,
        max_pool_overflow: int,
        pool_size: int,
    ) -> None:
        self.path_to_db = path_to_db
        self.logger = logger
        self.max_pool_overflow = max_pool_overflow
        self.pool_size = pool_size
        self.pool = self._initialize_connection_pool()

        self._initialize_db()

    def _initialize_connection_pool(self):
        pool = PooledDB(
            sqlite3,
            maxconnections=self.max_pool_overflow,
            mincached=self.pool_size,
            maxcached=self.pool_size,
            blocking=True,
            database=self.path_to_db,
        )
        return pool

    def _initialize_db(self):

        with self.pool.connection() as con:
            with con.cursor() as cur:
                sql_create_posts = """CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY NOT NULL,
                    title VARCHAR NOT NULL,
                    date VARCHAR NOT NULL,
                    content_md VARCHAR NOT NULL,
                    preview_md VARCHAR NOT NULL,
                    content_html VARCHAR NOT NULL,
                    preview_html VARCHAR NOT NULL);"""
                cur.executescript(sql_create_posts)

                sql_create_email = """CREATE TABLE IF NOT EXISTS email (
                    id INTEGER PRIMARY KEY NOT NULL,
                    date VARCHAR NOT NULL,
                    email_address VARCHAR NOT NULL UNIQUE,
                    confirmed VARCHAR NOT NULL);"""
                cur.executescript(sql_create_email)

                con.commit()

    def execute_read(self, sql: str, parameters: Tuple = (), fetch_one: bool = False) -> List[Tuple]|Tuple:

        with self.pool.connection() as con:
            with con.cursor() as cur:
                cur.execute(sql, parameters)

                if fetch_one:
                    result = cur.fetchone()
                else:
                    result = cur.fetchall()

        return result

    def execute_write(self, sql: str, parameters: Tuple = ()) -> None:

        with self.pool.connection() as con:
            with con.cursor() as cur:
                cur.execute(sql, parameters)
                con.commit()
