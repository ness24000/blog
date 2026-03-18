import re
from datetime import date
from logging import Logger
from typing import Tuple, List

import markdown
import numpy as np
from flask import Flask

from app.DBHandler import DBHandler
from app.MediaHandler import MediaHandler
from app.utils import get_date


class PostsHandler:
    def __init__(
        self, db_handler: DBHandler, media_handler: MediaHandler, logger: Logger
    ) -> None:
        self.db_handler = db_handler
        self.media_handler = media_handler
        self.logger = logger

    def _format_post_input(
        self, title: str, preview: str, content: str, post_id: int
    ) -> Tuple[str, ...]:
        IMG_PATTERN = r"!\[.*\]\("
        img_url_prefix = f"/media/{post_id}/"

        def produce_image_path(matchobj, img_url_prefix=img_url_prefix):
            return matchobj.group(0) + img_url_prefix

        content_html = re.sub(IMG_PATTERN, produce_image_path, content)

        content_html = markdown.markdown(content_html, extensions=["tables"])

        if preview == "":

            # if no preview provided, use content's first paragraph
            preview_html = str(
                re.findall("<p>.*?</p>", content_html, flags=re.DOTALL)[0]
            )
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

    def get_post(
        self, post_id=int, raw: bool = False, images_list: bool = False
    ) -> Tuple:

        sql = "SELECT title, date, preview_html, content_html FROM posts WHERE id = ?"
        if raw:
            sql = "SELECT title, date, preview_md, content_md FROM posts WHERE id = ?"

        post = self.db_handler.execute_read(
            sql,
            (post_id,),
            fetch_one=True,
        )
        if images_list:
            images_list = self.media_handler.list_images(post_id)
            post += (images_list,)

        return post

    def add_post(
        self,
        title: str,
        preview: str,
        content: str,
        images: List,
        return_rendered: bool = False,
    ) -> int | Tuple:

        current_date = get_date()

        # Insert first to obtain the DB-assigned id, used as the image folder name
        post_id = self.db_handler.execute_write(
            "INSERT INTO posts(title, date, preview_md, content_md, preview_html, content_html) VALUES (?,?,?,?,?,?)",
            (title, current_date, preview, content, "", ""),
        )

        title, preview_md, content_md, preview_html, content_html = (
            self._format_post_input(title, preview, content, post_id)
        )

        self.db_handler.execute_write(
            "UPDATE posts SET preview_md=?, content_md=?, preview_html=?, content_html=? WHERE id=?",
            (preview_md, content_md, preview_html, content_html, post_id),
        )

        self.logger.debug(f"Added post with title {title}, id {post_id}")

        if len(images) > 0:
            self.media_handler.save_images(images, post_id)

        if return_rendered:
            return post_id, preview_html, content_html
        return post_id

    def edit_post(
        self,
        post_id: int,
        title: str,
        preview: str,
        content: str,
        drop_images: List[str],
        new_images: List,
    ) -> None:

        title, preview_md, content_md, preview_html, content_html = (
            self._format_post_input(title, preview, content, post_id)
        )

        self.db_handler.execute_write(
            "UPDATE posts SET (title, preview_md, content_md, preview_html, content_html) = (?,?,?,?,?) where id = ?",
            (title, preview_md, content_md, preview_html, content_html, post_id),
        )

        self.media_handler.remove_selected_images(post_id, drop_images)
        self.media_handler.save_images(new_images, post_id)

        self.logger.debug(f"Updating post {post_id} with new title {title}")

    def delete_post(self, post_id: int) -> None:

        title = self.db_handler.execute_read(
            "select title from posts where id = ?", (post_id,), fetch_one=True
        )[0]
        self.logger.debug(f"Deleting post {post_id}, with title: {title}")

        self.media_handler.delete_images(post_id)
        self.db_handler.execute_write("delete from posts where id = ?;", (post_id,))
