import logging
import os
import re
import sqlite3


def initialize_db(path_to_db: str):

    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    sql_create_posts = """CREATE TABLE IF NOT EXISTS posts (
       id INTEGER PRIMARY KEY NOT NULL,
       title VARCHAR NOT NULL,
       date VARCHAR NOT NULL,
       content_md VARCHAR NOT NULL,
       preview_md VARCHAR NOT NULL,
       content_html VARCHAR NOT NULL,
       preview_html VARCHAR NOT NULL);"""
    cur.executescript(sql_create_posts)

    sql_create_mail = """CREATE TABLE IF NOT EXISTS mail (
       id INTEGER PRIMARY KEY NOT NULL,
       date VARCHAR NOT NULL,
       email_address VARCHAR NOT NULL,
       confirmed VARCHAR NOT NULL);"""
    cur.executescript(sql_create_mail)

    con.commit()


def connect_to_db(path_to_db: str):
    con = sqlite3.connect(path_to_db, check_same_thread=False)
    return con.cursor()


def add_post_to_db(
    title: str,
    date: str,
    preview_md: str,
    content_md: str,
    preview_html: str,
    content_html: str,
    path_to_db: str,
):

    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    cur.execute(
        "INSERT INTO posts(title, date, preview_md, content_md, preview_html, content_html) VALUES (?,?,?,?,?,?)",
        (title, date, preview_md, content_md, preview_html, content_html),
    )
    con.commit()


def update_post_in_db(
    post_id: int,
    title: str,
    preview_md: str,
    content_md: str,
    preview_html: str,
    content_html: str,
    path_to_db: str,
):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    cur.execute(
        "UPDATE posts SET (title, preview_md, content_md, preview_html, content_html) = (?,?,?,?,?) where id = ?",
        (title, preview_md, content_md, preview_html, content_html, post_id),
    )

    con.commit()


def delete_post_in_db(post_id: int, path_to_db: str):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    cur.execute("delete from posts where id = ?;", (post_id,))

    con.commit()
    pass
