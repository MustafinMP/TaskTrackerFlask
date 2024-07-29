from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, TextAreaField
from wtforms.fields import SelectField
from wtforms.validators import DataRequired

import db_session
from tasks.models import Status


class CreateTaskForm(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание задачи', validators=[DataRequired()])
    submit = SubmitField('Создать')


class ChangeStatusForm(FlaskForm):
    new_status: SelectField = SelectField('Статус задачи')
    submit = SubmitField('Сохранить')


class EditTaskForm(CreateTaskForm, ChangeStatusForm):
    ...


def get_statuses() -> list[Status]:
    session = db_session.create_session()
    return [(status.id, status.name) for status in session.query(Status).all()]
