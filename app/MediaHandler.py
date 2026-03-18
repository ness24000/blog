import os
import shutil
from logging import Logger

from werkzeug.utils import secure_filename


class MediaHandler:
    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}

    def __init__(self, path_to_media_folder: str, logger: Logger) -> None:
        self.path_to_media_folder = path_to_media_folder
        self.logger = logger

    def save_images(self, files, post_id: int) -> None:
        """Save uploaded image files to app/static/<post_id>/."""
        valid_files = [
            f
            for f in files
            if f
            and f.filename
            and "." in f.filename
            and f.filename.rsplit(".", 1)[1].lower()
            in MediaHandler.ALLOWED_IMAGE_EXTENSIONS
        ]
        if not valid_files:
            return
        folder = os.path.join(self.path_to_media_folder, str(post_id))
        os.makedirs(folder, exist_ok=True)
        for f in valid_files:
            f.save(os.path.join(folder, secure_filename(f.filename)))

    def delete_images(self, post_id: int) -> None:
        """Remove the image folder for a post, if it exists."""
        folder = os.path.join(self.path_to_media_folder, str(post_id))
        if os.path.isdir(folder):
            shutil.rmtree(folder, ignore_errors=True)

    def list_images(self, post_id: int) -> list[str]:
        """Return sorted list of image filenames for a post, or [] if none."""
        folder = os.path.join(self.path_to_media_folder, str(post_id))
        if not os.path.isdir(folder):
            return []
        return sorted(os.listdir(folder))

    def remove_selected_images(self, post_id: int, filenames: list[str]) -> None:
        """Delete specific image files from the post's static folder."""
        folder = os.path.join(self.path_to_media_folder, str(post_id))
        for name in filenames:
            target = os.path.join(folder, secure_filename(name))
            if os.path.isfile(target):
                os.remove(target)
