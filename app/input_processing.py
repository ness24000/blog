import re

import markdown

def format_post_input(title: str, preview: str, content: str):

    IMG_PATTERN = r"!\[.*\]\("
    img_folder = title.lower().replace(" ", "_")

    def produce_image_path(matchobj, img_folder=img_folder):
        return matchobj.group(0) + f"../static/{img_folder}/"

    content_html = re.sub(IMG_PATTERN, produce_image_path, content)

    content_html = markdown.markdown(content_html, extensions = ['tables'])

    if preview == "":

        # if no preview provided, use content's first paragraph
        preview_html = re.findall("<p>.*?</p>", content_html, flags=re.DOTALL)[0]
    else:
        preview_html = markdown.markdown(preview)

    return title, preview, content, preview_html, content_html
