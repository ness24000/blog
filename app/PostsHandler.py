from typing import Tuple, List
import re

import markdown
import numpy as np
from logging import Logger

from app.DBHandler import DBHandler


class PostsHandler:
    def __init__(self, db_handler: DBHandler, logger: Logger) -> None:
        self.db_handler = db_handler
        self.logger = logger

    def _format_post_input(self, title: str, preview: str, content: str) -> Tuple:
        IMG_PATTERN = r"!\[.*\]\("
        img_folder = title.lower().replace(" ", "_")

        def produce_image_path(matchobj, img_folder=img_folder):
            return matchobj.group(0) + f"../static/{img_folder}/"

        content_html = re.sub(IMG_PATTERN, produce_image_path, content)

        content_html = markdown.markdown(content_html, extensions=["tables"])

        if preview == "":

            # if no preview provided, use content's first paragraph
            preview_html = re.findall("<p>.*?</p>", content_html, flags=re.DOTALL)[0]
        else:
            preview_html = markdown.markdown(preview)

        return title, preview, content, preview_html, content_html

    def get_posts_overview(self) -> np.ndarray:
        posts = self.db_handler.execute_read(
            "SELECT id, title, date, preview_html FROM posts"
        )

        # latest first
        posts = np.flip(posts, axis=0)
        return posts

    def get_post(self, post_id=int) -> Tuple:
        post = self.db_handler.execute_read(
            "SELECT title, date, content_html FROM posts WHERE id = ?",
            (post_id,),
            fetch_one=True,
        )
        return post

    def add_post(self):
        pass

    def edit_post(self):
        pass

    def delete_post(self, post_id: int) -> None:
        self.db_handler.execute_write("delete from posts where id = ?;", (post_id,))
        self.logger.debug(f"Deleting post {post_id}")
