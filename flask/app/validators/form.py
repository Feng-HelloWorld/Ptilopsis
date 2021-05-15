from app.validators.base import BaseForm
from wtforms import StringField
from wtforms.validators import DataRequired


class TokenForm(BaseForm):
    username = StringField(validators=[DataRequired(message="Can't be empty")])
    password = StringField(validators=[DataRequired(message="Can't be empty")])