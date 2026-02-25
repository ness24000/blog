from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SelectMultipleField, PasswordField, SelectMultipleField, StringField, TextAreaField, validators
from wtforms.widgets import CheckboxInput, ListWidget


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class AddPostForm(FlaskForm):
    title = StringField("Title", [validators.input_required()])
    content = TextAreaField("Content", [validators.input_required()])
    preview = TextAreaField("Preview")
    images = MultipleFileField("Images")
    admin_key = PasswordField("Admin Key", [validators.input_required()])

class EditPostForm(AddPostForm):
    delete_images = MultiCheckboxField("Delete existing images", choices=[])

class DeletePostForm(FlaskForm):
    admin_key = PasswordField("Admin Key", [validators.input_required()])


class SubscribeToNewsletter(FlaskForm):
    email = StringField(
        "Email Address",
        [validators.input_required()],
    )
