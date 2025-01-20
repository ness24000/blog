from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    posts = pd.read_csv("./posts_df.csv").to_records()
    return render_template("index.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<int:post_id>")
def post(post_id):
    post = pd.read_csv("./posts_df.csv").to_records()[post_id]
    return render_template("post.html", post = post)
