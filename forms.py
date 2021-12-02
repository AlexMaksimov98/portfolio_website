from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, StringField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class ContactForm(FlaskForm):
    name = StringField('Your name', validators=[DataRequired()])
    email = StringField('Your email', validators=[DataRequired()])
    message = CKEditorField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
