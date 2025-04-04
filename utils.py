import re
import sqlite3

import markdown


def add_post_to_db(title, date, content, path_to_db):

    IMG_PATTERN = r"!\[.*\]\("
    img_folder = title.lower().replace(" ", "_")

    def produce_image_path(matchobj, img_folder=img_folder):
        return matchobj.group(0) + f"../static/{img_folder}/"

    content = re.sub(IMG_PATTERN, produce_image_path, content)

    content = markdown.markdown(content)

    preview = re.findall("<p>.*?</p>", content, flags=re.DOTALL)[0]

    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    cur.execute(
        "INSERT INTO posts(title, date, content, preview) VALUES (?,?,?,?)",
        (title, date, content, preview),
    )
    con.commit()
