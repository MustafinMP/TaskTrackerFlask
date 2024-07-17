from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateTaskForm(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание задачи', validators=[DataRequired()])
    submit = SubmitField('Создать')