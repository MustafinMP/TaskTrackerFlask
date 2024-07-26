from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CreateBasketForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание корзинки', validators=[DataRequired()])
    submit = SubmitField('Создать')