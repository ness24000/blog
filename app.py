from flask import Flask, render_template
import numpy as np
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("./posts.db",check_same_thread=False)
cur = con.cursor()

@app.route("/")
def index():
    posts = np.flip(cur.execute("SELECT * FROM posts").fetchall(),axis = 0)
    return render_template("index.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<int:post_id>")
def post(post_id):
    post = cur.execute("SELECT * FROM posts WHERE id = ?",[post_id]).fetchone()
    return render_template("post.html", post = post)
