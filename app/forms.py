from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators


class AddPostForm(FlaskForm):
    title = StringField("Title", [validators.input_required()])
    date = StringField("Date")
    content = TextAreaField("Content", [validators.input_required()])
