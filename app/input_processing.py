import re
from datetime import date

import markdown


def get_date():
    return date.today().strftime("%d %B %Y")


def format_post_input(title: str, preview: str, content: str):
    date = get_date()

    IMG_PATTERN = r"!\[.*\]\("
    img_folder = title.lower().replace(" ", "_")

    def produce_image_path(matchobj, img_folder=img_folder):
        return matchobj.group(0) + f"../static/{img_folder}/"

    content = re.sub(IMG_PATTERN, produce_image_path, content)

    content = markdown.markdown(content)

    if preview == "":

        # if no preview provided, use content's first paragraph
        preview = re.findall("<p>.*?</p>", content, flags=re.DOTALL)[0]
    else:
        preview = markdown.markdown(preview)

    return title, date, preview, content
