import numpy as np
from email_validator import EmailNotValidError, validate_email
from flask import redirect, render_template, request
from werkzeug.security import check_password_hash

from app import app, cur, logger
from app.db_interface import (add_email_to_db, add_post_to_db,
                              check_email_exists_in_db, delete_post_in_db,
                              email_confirmation_in_db, remove_email_from_db,
                              update_post_in_db)
from app.emailing import send_confirmation_email, send_newsletter
from app.forms import AddPostForm, DeletePostForm, SubscribeToNewsletter
from app.input_processing import format_post_input
from app.limiter import limiter
from app.utils import get_date, load_signed_data


@app.route("/")
def index():
    posts = np.flip(
        cur.execute("SELECT id, title, date, preview_html FROM posts").fetchall(),
        axis=0,
    )
    return render_template("index.html", posts=posts)


@app.route("/newsletter", methods=["GET", "POST"])
@limiter.limit("5 per day", methods=["POST"])
def newsletter():
    form = SubscribeToNewsletter()

    if form.validate_on_submit():

        # 1. validate email format
        try:
            emailinfo = validate_email(form.email.data)
            email_address = emailinfo.normalized
        except EmailNotValidError:
            form = SubscribeToNewsletter()
            form.email.data = ""  # explicitly clear the field
            placeholder_message = "This email seems invalid, try again"
            return render_template(
                "newsletter.html", form=form, placeholder=placeholder_message
            )

        # 2. check if email in db
        if check_email_exists_in_db(email_address, app.config["PATH_TO_DB"]):
            form = SubscribeToNewsletter()
            form.email.data = ""
            placeholder_message = "It seems you are already suscribed!"
            return render_template(
                "newsletter.html", form=form, placeholder=placeholder_message
            )

        # 3. try sending
        email_sent_status = send_confirmation_email(email_address, logger)

        if email_sent_status:
            add_email_to_db(email_address, app.config["PATH_TO_DB"])

            logger.debug(f"{form.email.data} suscribed [not confirmed]")
            return render_template("request_email_confirmation.html")

        else:
            logger.debug(
                f"Error sending email to {form.email.data}, check mailtrap logs"
            )
            form = SubscribeToNewsletter()
            form.email.data = ""
            placeholder_message = "Error processing your suscription, try again later"
            return render_template(
                "newsletter.html", form=form, placeholder=placeholder_message
            )

    return render_template("newsletter.html", form=form)


@app.route("/newsletter-confirmation/<string:signed_email_address>")
def newsletter_confirmation(signed_email_address):
    email_address = load_signed_data(
        signed_email_address,
        secret_key=app.config["ADMIN_KEY_HASH"],
        salt="confirmation",
    )
    try:
        email_confirmation_in_db(email_address, app.config["PATH_TO_DB"])
    except Exception:
        logger.error(
            f"Failed confirming email {email_address}, whith exception: {Exception}"
        )
        return "Oops, something went wrong. Try again later :)"

    logger.debug(f"{email_address} suscribed [confirmed]")
    return render_template("email_confirmed.html")


@app.route("/newsletter-unsubscribe/<string:signed_email_address>")
def newsletter_unsubscribe(signed_email_address):
    email_address = load_signed_data(
        signed_email_address,
        secret_key=app.config["ADMIN_KEY_HASH"],
        salt="unsubscribe",
    )
    try:
        remove_email_from_db(email_address, app.config["PATH_TO_DB"])
    except Exception:
        logger.error(
            f"Failed unsubscribing email {email_address}, whith exception: {Exception}"
        )
        return "Oops, something went wrong. Try again later :)"

    logger.debug(f"{email_address} unsubscribed")
    return render_template("unsubscribed.html")


@app.route("/post/<int:post_id>")
def post(post_id):
    post = cur.execute(
        "SELECT title, date, content_html FROM posts WHERE id = ?", [post_id]
    ).fetchone()
    return render_template("post.html", post=post)


@app.route("/add_post", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods = ["POST"])
def add_post():
    form = AddPostForm()

    if request.method == "POST":
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("add_post.html", form=form)

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

        # email everyone in newsletter
        send_newsletter.delay(title, preview_html, app.config["ADMIN_KEY_HASH"])

        return redirect("/")

    return render_template("add_post.html", form=form)


@app.route("/edit_post/")
def list_posts_edit():
    posts = np.flip(cur.execute("SELECT id, title FROM posts").fetchall(), axis=0)
    return render_template("list_posts.html", posts=posts)


@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def edit_post(post_id):

    form = AddPostForm()

    if request.method == "POST":
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("add_post.html", form=form)

    # POST: format input run as in add post, use app.db_interface.update_post_in_db
    if form.validate_on_submit():
        logger.debug(f"Updating post {post_id}  with new title {form.title.data}")

        title, preview_md, content_md, preview_html, content_html = format_post_input(
            form.title.data, form.preview.data, form.content.data
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
@limiter.limit("5 per minute", methods=["POST"])
def delete_post(post_id):

    form = DeletePostForm()

    if request.method == "POST":
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("delete_post.html", form=form)

    # POST: format input run as in add post, use app.db_interface.update_post_in_db
    if form.validate_on_submit():
        logger.debug(f"Deleting post {post_id}")
        delete_post_in_db(post_id, app.config["PATH_TO_DB"])

        return redirect("/")

    # GET: return form to include password
    return render_template("delete_post.html", form=form)
