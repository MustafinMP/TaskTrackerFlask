from flask import Blueprint, redirect, render_template, request, abort, jsonify
from flask_login import login_required, current_user
from sqlalchemy import and_, select

import db_session
from backend.tasks.forms import CreateTaskForm, ChangeStatusForm, EditTaskForm, create_change_status_form, \
    create_edit_task_form
from tasks.models import Task, Status

blueprint = Blueprint('tasks', __name__)
prefix: str = '/tasks'


@blueprint.route('/')
def tasks_by_statuses():
    if current_user.is_authenticated:
        with db_session.create_session() as session:
            statuses: list[Status] = session.scalars(select(Status)).all()
            statuses.sort(key=lambda status: status.id)
            tasks_: dict[int, list[Task | None]] = {
                status.id: session.scalars(
                    select(Task).where(
                        and_(
                            Task.creator_id == current_user.id,
                            Task.status_id == status.id
                        )
                    )
                ).all()
                for status in statuses
            }
            return render_template(prefix + '/tasks_by_statuses.html',
                                   statuses=statuses,
                                   tasks_by_statuses=tasks_)
    return redirect('/')


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = CreateTaskForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        task = Task()
        task.name = form.name.data
        task.description = form.description.data
        task.creator_id = current_user.get_id()
        if (status := request.args.get('status', None)) is not None:
            task.status_id = status
        session.add(task)
        session.commit()
        return redirect('/tasks')
    return render_template(prefix + '/create.html', form=form, title='Добавить задачу')


@blueprint.route('/<int:task_id>', methods=['GET', 'POST'])
@login_required
def show_task(task_id: int):
    if not current_user.is_authenticated:
        return abort(404)
    with db_session.create_session() as session:
        task: Task = session.query(Task).where(
            and_(current_user.id == Task.creator_id, Task.id == task_id)).one_or_none()
        if task is None or task.creator_id != current_user.id:
            return abort(404)
        form: ChangeStatusForm = create_change_status_form(task)
        if request.method == 'POST' and form.validate_on_submit():
            new_status_id: int = form.new_status.data
            task.status_id = new_status_id
            session.commit()
            return render_template(prefix + '/show_task.html', task=task, form=form, save=True)
        return render_template(prefix + '/show_task.html', task=task, form=form, save=False)


@blueprint.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id: int):
    with db_session.create_session() as session:
        task: Task = session.query(Task).where(Task.id == task_id).one_or_none()
        if task is None or task.creator_id != current_user.id:
            return abort(404)
        form: EditTaskForm = create_edit_task_form(task)
        if request.method == 'GET':
            form.name.data = task.name
            form.description.data = task.description
            return render_template(prefix + '/edit.html', form=form, title='Изменить задачу')
        if form.validate_on_submit:
            task: Task = session.query(Task).where(Task.id == task_id).first()
            task.name = form.name.data
            task.description = form.description.data
            task.status_id = form.new_status.data
            session.commit()
            return redirect(f'/tasks/{task_id}')


@blueprint.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id: int):
    with db_session.create_session() as session:
        task: Task = session.query(Task).where(Task.id == task_id).one_or_none()
        if task is None or task.creator_id != current_user.id:
            return abort(404)
        session.delete(task)
        session.commit()
        return redirect('/tasks')


@blueprint.route('/get')
@login_required
def get():
    with db_session.create_session() as session:
        tasks: list[Task] = session.query(Task).where(
            and_(current_user.id == Task.creator_id)).all()
        return jsonify(
            {
                'tasks': [task.to_dict(only=('name', 'creator.name', 'description', 'status')) for task in tasks]
            }
        )
