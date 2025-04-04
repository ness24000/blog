import logging
import sqlite3

import numpy as np
from flask import Flask, jsonify, redirect, render_template, request

from config import Config
from forms import AddPostForm
from utils import add_post_to_db

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")

app = Flask(__name__)
app.config.from_object(Config)

con = sqlite3.connect("./posts.db", check_same_thread=False)
cur = con.cursor()


@app.route("/")
def index():
    posts = np.flip(cur.execute("SELECT * FROM posts").fetchall(), axis=0)
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:post_id>")
def post(post_id):
    post = cur.execute("SELECT * FROM posts WHERE id = ?", [post_id]).fetchone()
    return render_template("post.html", post=post)


@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        logger.debug(f"Adding post with title {form.title.data}")
        add_post_to_db(
            form.title.data,
            form.date.data,
            form.content.data,
            "posts.db",
        )

        return redirect("/")

    return render_template("add_post.html", form=form)
