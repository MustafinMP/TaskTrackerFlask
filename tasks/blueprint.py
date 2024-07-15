from flask import Blueprint, redirect, render_template
from flask_login import login_required, current_user

import db_session
from tasks.forms import CreateTaskForm
from tasks.models import Task

blueprint = Blueprint('tasks', __name__)
prefix: str = '/tasks'
path: str = prefix + '/'


@blueprint.route('/')
def all_tasks():
    data: list = list()
    if current_user.is_authenticated:
        session = db_session.create_session()
        data: list = session.query(Task).where(current_user.id == Task.creator).all()
    print(data)
    return render_template(path + 'tasks.html', data=data)


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def add_news():
    form = CreateTaskForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        task = Task()
        task.name = form.name.data
        task.description = form.description.data
        task.creator = current_user.get_id()
        session.add(task)
        session.commit()
        return redirect('/')
    return render_template(path + 'create.html', form=form)