from flask import Blueprint, redirect, render_template, request, abort
from flask_login import login_required, current_user
from sqlalchemy import or_, and_

import db_session
from tasks.forms import CreateTaskForm, ChangeStatusForm, get_statuses
from tasks.models import Task, Status

blueprint = Blueprint('tasks', __name__)
prefix: str = '/tasks'
path: str = prefix + '/'


@blueprint.route('/')
def all_tasks():
    data: list = list()
    if current_user.is_authenticated:
        session = db_session.create_session()
        data: list = session.query(Task).where(current_user.id == Task.creator_id).all()
    return render_template(path + 'tasks.html', data=data)


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def add_task():
    form = CreateTaskForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        task = Task()
        task.name = form.name.data
        task.description = form.description.data
        task.creator_id = current_user.get_id()
        session.add(task)
        session.commit()
        return redirect('/tasks')
    return render_template(path + 'create.html', form=form)


@blueprint.route('/<int:task_id>', methods=['GET', 'POST'])
@login_required
def show_task(task_id: int):
    if not current_user.is_authenticated:
        return abort(404)
    with db_session.create_session() as session:
        task: Task = session.query(Task).where(
            and_(current_user.id == Task.creator_id, Task.id == task_id)).first()
        if not task:
            return abort(404)
        form = ChangeStatusForm(new_status=task.status_id)
        form.new_status.choices = get_statuses()
        if request.method == 'POST' and form.validate_on_submit():
            new_status_id: int = form.new_status.data
            task.status_id = new_status_id
            session.commit()
            return render_template(path + 'show_task.html', task=task, form=form, save=True)
        return render_template(path + 'show_task.html', task=task, form=form, save=False)


@blueprint.route('/edit/<task_id>', methods=['GET', 'PUT'])
@login_required
def edit_task(task_id: int):  # TODO: put request
    if request.method == 'GET':
        form = CreateTaskForm()
        session = db_session.create_session()
        task: Task = session.query(Task).where(Task.id == task_id).first()
        form.name.data = task.name
        form.description.data = task.description
        return render_template(path + 'create.html', form=form)
