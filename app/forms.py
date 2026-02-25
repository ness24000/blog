from flask_wtf import FlaskForm
from wtforms import MultipleFileField, PasswordField, StringField, TextAreaField, validators


class AddPostForm(FlaskForm):
    title = StringField("Title", [validators.input_required()])
    content = TextAreaField("Content", [validators.input_required()])
    preview = TextAreaField("Preview")
    images = MultipleFileField("Images")
    admin_key = PasswordField("Admin Key", [validators.input_required()])


class DeletePostForm(FlaskForm):
    admin_key = PasswordField("Admin Key", [validators.input_required()])


class SubscribeToNewsletter(FlaskForm):
    email = StringField(
        "Email Address",
        [validators.input_required()],
    )
