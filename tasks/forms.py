from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateTaskForm(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired()])
    description = StringField('Описание задачи', validators=[DataRequired()])
    submit = SubmitField('Создать')