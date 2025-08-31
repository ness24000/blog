import numpy as np
from flask import jsonify, redirect, render_template, request
from werkzeug.security import check_password_hash
from email_validator import validate_email, EmailNotValidError

from app import app, cur, logger
from app.db_interface import add_post_to_db, update_post_in_db, delete_post_in_db
from app.forms import AddPostForm, DeletePostForm, SubscribeToNewsletter
from app.input_processing import format_post_input
from app.limiter import limiter
from app.utils import get_date
from app.mailing import sending_test_email

@app.route("/")
def index():
    posts = np.flip(
        cur.execute("SELECT id, title, date, preview_html FROM posts").fetchall(),
        axis=0,
    )
    return render_template("index.html", posts=posts)


@app.route("/newsletter", methods=["GET", "POST"])
def newsletter():
    form = SubscribeToNewsletter()
    
    if form.validate_on_submit():

        try: 
            emailinfo = validate_email(form.email.data)
            email = emailinfo.normalized
        except EmailNotValidError:
            form = SubscribeToNewsletter()
            form.email.data = ""  # explicitly clear the field
            return render_template("newsletter.html", form = form, first_attempt = False)

        # validate email 
        # send validation email 
        # if sending fails, return the template again, with the form saying ooh it failed

        # add non confirmed entry in db

        logger.debug(f"{form.email.data} suscribed [not confirmed]")
        return "Valid"

            
        
        
        
    return render_template("newsletter.html", form = form, first_attempt = True)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = cur.execute(
        "SELECT title, date, content_html FROM posts WHERE id = ?", [post_id]
    ).fetchone()
    return render_template("post.html", post=post)


@app.route("/add_post", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def add_post():
    form = AddPostForm()

    if request.method == "POST":
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("add_post.html", form=form)

    if form.validate_on_submit():
        logger.debug(f"Adding post with title {form.title.data}")

        title, preview_md, content_md, preview_html, content_html = format_post_input(
            form.title.data, form.preview.data, form.content.data
        )
        date = get_date()

        add_post_to_db(
            title,
            date,
            preview_md,
            content_md,
            preview_html,
            content_html,
            app.config["PATH_TO_DB"],
        )

        return redirect("/")

    return render_template("add_post.html", form=form)

@app.route("/edit_post/")
def list_posts_edit():
    posts = np.flip(cur.execute("SELECT id, title FROM posts").fetchall(), axis=0)
    return render_template("list_posts.html", posts=posts)

@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def edit_post(post_id):

    form = AddPostForm()

    if request.method == "POST":
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("add_post.html", form=form)

    # POST: format input run as in add post, use app.db_interface.update_post_in_db
    if form.validate_on_submit():
        logger.debug(f"Updating post {post_id}  with new title {form.title.data}")

        title, preview_md, content_md, preview_html, content_html = (
            format_post_input(form.title.data, form.preview.data, form.content.data)
        )
        update_post_in_db(
            post_id,
            title,
            preview_md,
            content_md,
            preview_html,
            content_html,
            app.config["PATH_TO_DB"],
        )

        return redirect("/")

    # GET: return the edit_post.html with filled fields
    pos_id, title, date, preview_md, content_md = cur.execute(
        "SELECT id, title, date, preview_md, content_md FROM posts WHERE id=?",
        [post_id],
    ).fetchone()
    form = AddPostForm(title=title, date=date, content=content_md, preview=preview_md)

    return render_template("add_post.html", form=form, update=True)

@app.route("/delete_post/<int:post_id>", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def delete_post(post_id):

    form = DeletePostForm()

    if request.method == "POST":
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("delete_post.html", form=form)

    # POST: format input run as in add post, use app.db_interface.update_post_in_db
    if form.validate_on_submit():
        logger.debug(f"Deleting post {post_id}")       
        delete_post_in_db(post_id,app.config["PATH_TO_DB"])

        return redirect("/")

    # GET: return form to include password
    return render_template("delete_post.html", form=form)

@app.route("/send_test_email")
def send_test_email():
    response = sending_test_email()
    return response
