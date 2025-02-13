import markdown
import typer
import re

IMG_PATTERN = r"!\[.*\]\("

def main(file_name:str):

    with open(file_name, "r") as file: 
        title, date, content = re.split("\n+",file.read(), maxsplit=2)

    img_folder = title.lower().replace(" ", "_")
    def produce_image_path(matchobj, img_folder = img_folder):
        return matchobj.group(0) + f"../static/{img_folder}/"
    
    content = re.sub(IMG_PATTERN, produce_image_path, content)

    print("title", title)
    print("date", date)
    print("content", markdown.markdown(content))


if __name__ == "__main__":
    typer.run(main)
