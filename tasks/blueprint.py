from flask import Blueprint, redirect, render_template
from flask_login import login_required, current_user

import db_session
from tasks.forms import CreateTaskForm
from tasks.models import Task

blueprint = Blueprint('tasks', __name__)


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def add_news():
    form = CreateTaskForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        task = Task()
        task.name = form.name.data
        task.description = form.description.data
        task.creator = current_user.get_id()
        db_sess.add(task)
        db_sess.commit()
        return redirect('/')
    return render_template('tasks/create.html', form=form)