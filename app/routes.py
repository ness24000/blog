import os
import shutil

from flask import redirect, render_template, request
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from app import app, logger, posts_handler, mail_handler, limiter
from app.forms import AddPostForm, DeletePostForm, EditPostForm, SubscribeToNewsletter


ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}


def _save_images(files, post_id: int) -> None:
    """Save uploaded image files to app/static/<post_id>/."""
    valid_files = [
        f for f in files
        if f and f.filename and "." in f.filename
        and f.filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    ]
    if not valid_files:
        return
    folder = os.path.join(app.root_path, "static", str(post_id))
    os.makedirs(folder, exist_ok=True)
    for f in valid_files:
        f.save(os.path.join(folder, secure_filename(f.filename)))


def _delete_images(post_id: int) -> None:
    """Remove the image folder for a post, if it exists."""
    folder = os.path.join(app.root_path, "static", str(post_id))
    shutil.rmtree(folder, ignore_errors=True)


def _list_images(post_id: int) -> list[str]:
    """Return sorted list of image filenames for a post, or [] if none."""
    folder = os.path.join(app.root_path, "static", str(post_id))
    if not os.path.isdir(folder):
        return []
    return sorted(os.listdir(folder))


def _remove_selected_images(post_id: int, filenames: list[str]) -> None:
    """Delete specific image files from the post's static folder."""
    folder = os.path.join(app.root_path, "static", str(post_id))
    for name in filenames:
        target = os.path.join(folder, secure_filename(name))
        if os.path.isfile(target):
            os.remove(target)


@app.errorhandler(429)
def ratelimit_handler(e):
    logger.warning(f"Rate limit reached: {e}")
    return redirect("https://en.wikipedia.org/wiki/Rate_limiting")


@app.route("/")
def index():
    posts = posts_handler.get_posts_overview()
    return render_template("index.html", posts=posts)


@app.route("/newsletter", methods=["GET", "POST"])
@limiter.limit("5 per day", methods=["POST"])
def newsletter():
    form = SubscribeToNewsletter()

    if form.validate_on_submit():

        add_email_status = mail_handler.add_email(form.email.data)

        if add_email_status != "no_error":

            # show message corresponding to add_email error
            form = SubscribeToNewsletter()
            form.email.data = ""
            placeholder_message_dict = {
                "validation_error": "This email seems invalid, try again",
                "not_new_error": "It seems you are already suscribed!",
                "sending_error": "Error processing your suscription, try again later",
            }

            return render_template(
                "newsletter.html",
                form=form,
                placeholder=placeholder_message_dict[add_email_status],
            )
        else:
            return render_template("request_email_confirmation.html")

    return render_template("newsletter.html", form=form)


@app.route("/newsletter-confirmation/<string:signed_email_address>")
def newsletter_confirmation(signed_email_address):

    if mail_handler.confirm_email(signed_email_address):
        return render_template("email_confirmed.html")
    else:
        return "Oops, something went wrong. Try again later :)"


@app.route("/newsletter-unsubscribe/<string:signed_email_address>")
def newsletter_unsubscribe(signed_email_address):

    if mail_handler.delete_email(signed_email_address):
        return render_template("unsubscribed.html")
    else:
        return "Oops, something went wrong. Try again later :)"


@app.route("/post/<int:post_id>")
def post(post_id):
    post = posts_handler.get_post(post_id)
    return render_template("post.html", post=post)


@app.route("/add_post", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def add_post():
    form = AddPostForm()

    if form.validate_on_submit():
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("add_post.html", form=form)

        post_id, preview_html, _ = posts_handler.add_post(
            form.title.data, form.preview.data, form.content.data, return_rendered=True
        )

        _save_images(request.files.getlist("images"), post_id)
        mail_handler.send_newsletter(form.title.data, preview_html)
        return redirect("/")

    return render_template("add_post.html", form=form)


@app.route("/edit_post/")
def list_posts_edit():
    posts = posts_handler.get_posts_overview()
    return render_template("list_posts.html", posts=posts)


@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def edit_post(post_id):

    existing_images = _list_images(post_id)
    form = EditPostForm()
    form.delete_images.choices = [(img, img) for img in existing_images]

    if form.validate_on_submit():
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("add_post.html", form=form, update=True)

        posts_handler.edit_post(
            post_id, form.title.data, form.preview.data, form.content.data
        )
        _remove_selected_images(post_id, form.delete_images.data)
        _save_images(request.files.getlist("images"), post_id)
        return redirect("/")

    # GET: return the add_post.html with filled fields
    title, date, preview_md, content_md = posts_handler.get_post(post_id, raw=True)
    form = EditPostForm(title=title, date=date, content=content_md, preview=preview_md)
    form.delete_images.choices = [(img, img) for img in existing_images]

    return render_template("add_post.html", form=form, update=True)


@app.route("/delete_post/<int:post_id>", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def delete_post(post_id):

    form = DeletePostForm()

    if form.validate_on_submit():
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("delete_post.html", form=form)
        
        posts_handler.delete_post(post_id)
        _delete_images(post_id)
        return redirect("/")

    return render_template("delete_post.html", form=form)
