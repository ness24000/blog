import os
import shutil

from flask import redirect, render_template, request, send_from_directory
from werkzeug.security import check_password_hash

from app import app, limiter, logger, mail_handler, posts_handler
from app.forms import AddPostForm, DeletePostForm, EditPostForm, SubscribeToNewsletter


@app.route("/media/<int:post_id>/<path:filename>")
def media(post_id, filename):
    folder = os.path.join(app.config["PATH_TO_MEDIA_FOLDER"], str(post_id))
    return send_from_directory(folder, filename)


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
            form.title.data,
            form.preview.data,
            form.content.data,
            request.files.getlist("images"),
            return_rendered=True,
        )

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

    # We must define form.delete_images.choices here, to allow for validation. 
    # Thus this code must run always, even in a post request. Not ideal. 
    title, date, preview_md, content_md, image_list = posts_handler.get_post(
        post_id, raw=True, images_list=True
    )
    form = EditPostForm()
    form.delete_images.choices = [(img, img) for img in image_list]
    
    if form.validate_on_submit():
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("add_post.html", form=form, update=True)

        posts_handler.edit_post(
            post_id,
            form.title.data,
            form.preview.data,
            form.content.data,
            form.delete_images.data,
            request.files.getlist("images")
        )
        
        return redirect("/")

    # GET: return the add_post.html with filled fields
    form = EditPostForm(title=title, date=date, content=content_md, preview=preview_md)
    
    return render_template("add_post.html", form=form, update=True)


@app.route("/delete_post/<int:post_id>", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def delete_post(post_id):

    form = DeletePostForm()

    if form.validate_on_submit():
        if not check_password_hash(app.config["ADMIN_KEY_HASH"], form.admin_key.data):
            return render_template("delete_post.html", form=form)

        posts_handler.delete_post(post_id)
        return redirect("/")

    return render_template("delete_post.html", form=form)
