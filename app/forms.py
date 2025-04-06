from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, validators


class AddPostForm(FlaskForm):
    title = StringField("Title", [validators.input_required()])
    date = StringField("Date", [validators.input_required()])
    content = TextAreaField("Content", [validators.input_required()])
    admin_key = PasswordField("Admin Key", [validators.input_required()])
