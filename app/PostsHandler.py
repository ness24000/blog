import re
from datetime import date
from logging import Logger
from typing import Tuple

import markdown
import numpy as np
from app.utils import get_date

from app.DBHandler import DBHandler


class PostsHandler:
    def __init__(self, db_handler: DBHandler, logger: Logger) -> None:
        self.db_handler = db_handler
        self.logger = logger

    def _format_post_input(self, title: str, preview: str, content: str) -> Tuple[str, ...]:
        IMG_PATTERN = r"!\[.*\]\("
        img_folder = title.lower().replace(" ", "_")

        def produce_image_path(matchobj, img_folder=img_folder):
            return matchobj.group(0) + f"../static/{img_folder}/"

        content_html = re.sub(IMG_PATTERN, produce_image_path, content)

        content_html = markdown.markdown(content_html, extensions=["tables"])

        if preview == "":

            # if no preview provided, use content's first paragraph
            preview_html = str(re.findall("<p>.*?</p>", content_html, flags=re.DOTALL)[0])
        else:
            preview_html = markdown.markdown(preview)

        return title, preview, content, preview_html, content_html

    def get_posts_overview(self) -> np.ndarray:
        posts = self.db_handler.execute_read(
            "SELECT id, title, date, preview_html FROM posts"
        )

        # sort so last in first out
        posts = np.flip(posts, axis=0)
        return posts

    def get_post(self, post_id=int, raw: bool = False) -> Tuple:

        sql = "SELECT title, date, preview_html, content_html FROM posts WHERE id = ?"
        if raw:
            sql = "SELECT title, date, preview_md, content_md FROM posts WHERE id = ?"

        post = self.db_handler.execute_read(
            sql,
            (post_id,),
            fetch_one=True,
        )
        return post

    def add_post(self, title: str, preview: str, content: str, return_rendered: bool = False) -> None|Tuple[str, str]:

        title, preview_md, content_md, preview_html, content_html = (
            self._format_post_input(title, preview, content)
        )

        current_date = get_date()

        self.db_handler.execute_write(
            "INSERT INTO posts(title, date, preview_md, content_md, preview_html, content_html) VALUES (?,?,?,?,?,?)",
            (title, current_date, preview_md, content_md, preview_html, content_html),
        )

        self.logger.debug(f"Added post with title {title}")

        if return_rendered:
            return preview_html, content_html

    def edit_post(self, post_id: int, title: str, preview: str, content: str) -> None:

        title, preview_md, content_md, preview_html, content_html = (
            self._format_post_input(title, preview, content)
        )

        self.db_handler.execute_write(
            "UPDATE posts SET (title, preview_md, content_md, preview_html, content_html) = (?,?,?,?,?) where id = ?",
            (title, preview_md, content_md, preview_html, content_html, post_id),
        )

        self.logger.debug(f"Updating post {post_id} with new title {title}")

    def delete_post(self, post_id: int) -> None:
        self.db_handler.execute_write("delete from posts where id = ?;", (post_id,))
        self.logger.debug(f"Deleting post {post_id}")
