from flask import Blueprint, redirect, render_template
from flask_login import login_user, logout_user, login_required, current_user


import db_session
from auth.forms import LoginForm, RegisterForm
from auth.models import User
import auth.service as auth_srv
from tasks.models import Task, Status

blueprint = Blueprint('auth', __name__)
prefix = '/auth'


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                prefix + '/register.html',
                title='Регистрация',
                form=form,
                message="Пароли не совпадают"
            )
        if auth_srv.user_exists_by_email(form.email.data):
            return render_template(
                prefix + '/register.html',
                title='Регистрация',
                form=form,
                message="Такой пользователь уже есть"
            )
        auth_srv.create_user(form)
        return redirect(prefix + '/login')
    return render_template(prefix + '/register.html', title='Регистрация', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user: User = auth_srv.select_user_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/tasks")
        return render_template(prefix + '/login.html', message="Неправильный логин или пароль", form=form)
    return render_template(prefix + '/login.html', title='Авторизация', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/profile')
@login_required
def profile():
    with db_session.create_session() as session:
        tasks: list[Task] = session.query(Task).where(current_user.id == Task.creator_id).all()
        statuses: list[Status] = session.query(Status).all()
        tasks_count: dict[str, int] = {status.name: 0 for status in statuses}
        for task in tasks:
            tasks_count[task.status.name] += 1
    return render_template(prefix + '/profile.html', tasks_count=tasks_count)


@blueprint.route('/profile/edit')
@login_required
def edit_profile():
    return render_template(prefix + '/profile.html')