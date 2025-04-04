from flask_wtf import FlaskForm
from wtforms import StringField


class AddPostForm(FlaskForm):
    title = StringField("Title")
    date = StringField("Date")
    content = StringField("Content")
    
