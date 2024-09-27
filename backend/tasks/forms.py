from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.fields.simple import StringField, SubmitField, TextAreaField
from wtforms.fields import SelectField
from wtforms.validators import DataRequired, ValidationError, Optional

import db_session
from config import MIN_DEADLINE_GAP
from tasks.models import Status, Task


def deadline_required(form, field):
    if field.data and field.data < datetime.now() + MIN_DEADLINE_GAP:
        raise ValidationError('Deadline must be early than today')


class CreateTaskForm(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание задачи', validators=[DataRequired()])
    deadline = DateTimeLocalField('Дата окончания', validators=[deadline_required, Optional()])
    submit = SubmitField('Создать')


class ChangeStatusForm(FlaskForm):
    new_status: SelectField = SelectField('Статус задачи')
    submit = SubmitField('Сохранить')


class CreateTagForm(FlaskForm):
    name = StringField('Тег', validators=[DataRequired()])
    submit = SubmitField('Создать')


def create_change_status_form(task: Task):
    form = ChangeStatusForm(new_status=task.status_id)
    form.new_status.choices = get_statuses()
    return form


class EditTaskForm(ChangeStatusForm, CreateTaskForm):
    ...


def get_statuses() -> list[Status]:
    session = db_session.create_session()
    return [(status.id, status.name) for status in session.query(Status).all()]


def create_edit_task_form(task: Task):
    form = EditTaskForm(new_status=task.status_id)
    form.new_status.choices = get_statuses()
    return form
