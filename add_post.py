import markdown
import typer

def main(file_name:str):

    with open(file_name, "r") as file: 
        title, date, content = file.read().split("\n\n",2)

    content = content.replace("![](", f"![an image](../static/{title.lower().replace(" ", "_")}/")


if __name__ == "__main__":
    typer.run(main)
