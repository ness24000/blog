import markdown
import typer
import re
import sqlite3

IMG_PATTERN = r"!\[.*\]\("

def main(file_name:str, path_to_db: str = "posts.db"):

    with open(file_name, "r") as file: 
        title, date, content = re.split("\n+",file.read(), maxsplit=2)

    img_folder = title.lower().replace(" ", "_")
    def produce_image_path(matchobj, img_folder = img_folder):
        return matchobj.group(0) + f"../static/{img_folder}/"
    
    content = re.sub(IMG_PATTERN, produce_image_path, content)

    content = markdown.markdown(content)

    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    cur.execute("INSERT INTO posts(title, date,content) VALUES (?,?,?)", (title, date, content))
    con.commit()

    print(f"The image folder should be called:\n{img_folder}")

if __name__ == "__main__":
    typer.run(main)
