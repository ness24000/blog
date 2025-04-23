import numpy as np
from flask import jsonify, redirect, render_template, request
from werkzeug.security import check_password_hash

from app import app, cur, logger
from app.forms import AddPostForm
from app.db_interface import add_post_to_db


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

    if request.method == "POST":
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("add_post.html", form=form)

    if form.validate_on_submit():
        logger.debug(f"Adding post with title {form.title.data}")
        add_post_to_db(
            form.title.data,
            form.preview.data,
            form.content.data,
            app.config["PATH_TO_DB"],
        )

        return redirect("/")

    return render_template("add_post.html", form=form)
