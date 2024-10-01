from flask import Blueprint, redirect, render_template, request, abort
from flask_login import login_required, current_user

from tasks.forms import CreateTaskForm, ChangeStatusForm, EditTaskForm, create_change_status_form, \
    create_edit_task_form
from tasks.models import Task, Status
import tasks.service as task_service

blueprint = Blueprint('tasks', __name__)
prefix: str = '/tasks'


@blueprint.route('/')
def tasks_by_statuses():
    if current_user.is_authenticated:
        statuses: list[Status, ...] = task_service.get_all_statuses()
        statuses.sort(key=lambda status: status.id)

        tasks: dict[int, list[Task, ...]] = {
            status.id: task_service.get_task_by_status(status.id)
            for status in statuses
        }

        return render_template(prefix + '/tasks_by_statuses.html',
                               statuses=statuses,
                               tasks_by_statuses=tasks)
    return redirect('/')


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = CreateTaskForm()
    if form.validate_on_submit():
        task_service.add_task(
            form.name.data,
            form.description.data,
            form.deadline.data,
            request.args.get('status', None)
        )
        return redirect('/tasks')
    return render_template(prefix + '/create.html', form=form, title='Добавить задачу')


@blueprint.route('/<int:task_id>', methods=['GET', 'POST'])
@login_required
def show_task(task_id: int):
    if (task := task_service.get_task_by_id(task_id)) is None:
        return abort(404)

    form: ChangeStatusForm = create_change_status_form(task)
    if form.validate_on_submit():
        task_service.update_task(task_id, new_status_id=form.new_status.data)
        task = task_service.get_task_by_id(task_id)
        return render_template(prefix + '/show_task.html', task=task, form=form, save=True)
    return render_template(prefix + '/single_task.html', task=task, form=form, save=False)


@blueprint.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id: int):
    if (task := task_service.get_task_by_id(task_id)) is None:
        return abort(404)
    form: EditTaskForm = create_edit_task_form(task)

    if request.method == 'GET':
        form.name.data = task.name
        form.description.data = task.description
        return render_template(prefix + '/edit.html', form=form, title='Изменить задачу')

    if form.validate_on_submit:
        task_service.update_task(task_id, form.name.data, form.description.data, form.new_status.data)
        return redirect(f'/tasks/{task_id}')


@blueprint.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id: int):
    if task_service.get_task_by_id(task_id) is None:
        return abort(404)
    task_service.delete_task(task_id)
    return redirect('/tasks')
