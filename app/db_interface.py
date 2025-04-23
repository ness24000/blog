import logging
import os
import re
import sqlite3

import markdown

from app.utils import get_date


def initialize_db(path_to_db: str):

    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    sql_create_posts = """CREATE TABLE IF NOT EXISTS posts (
       id INTEGER PRIMARY KEY NOT NULL,
       title VARCHAR NOT NULL UNIQUE,
       date VARCHAR NOT NULL,
       content VARCHAR NOT NULL,
       preview VARCHAR NOT NULL);"""

    cur.executescript(sql_create_posts)
    con.commit()


def connect_to_db(path_to_db: str):
    con = sqlite3.connect(path_to_db, check_same_thread=False)
    return con.cursor()

def add_post_to_db(title: str, preview: str, content: str, path_to_db: str):

    date = get_date()

    IMG_PATTERN = r"!\[.*\]\("
    img_folder = title.lower().replace(" ", "_")

    def produce_image_path(matchobj, img_folder=img_folder):
        return matchobj.group(0) + f"../static/{img_folder}/"

    content = re.sub(IMG_PATTERN, produce_image_path, content)

    content = markdown.markdown(content)

    if preview == '':

        # if no preview provided, use content's first paragraph
        preview = re.findall("<p>.*?</p>", content, flags=re.DOTALL)[0]
    else:
        preview = markdown.markdown(preview)

    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    cur.execute(
        "INSERT INTO posts(title, date, content, preview) VALUES (?,?,?,?)",
        (title, date, content, preview),
    )
    con.commit()

def update_post(title: str, preview: str, content: str, path_to_db: str):
    pass
