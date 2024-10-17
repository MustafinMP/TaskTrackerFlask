import requests
from flask import Blueprint, redirect, render_template, request
from flask_login import login_user, logout_user, login_required, current_user

import db_session
from auth.exceptions import UserDoesNotExistError
from auth.forms import LoginForm, RegisterForm
from auth.models import User
import auth.service as auth_srv
from config import YANDEX_API_REQUEST, YA_CLIENT_ID, YA_CLIENT_SECRET
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
        auth_srv.add_user(form)
        return redirect(prefix + '/login')
    return render_template(prefix + '/register.html', title='Регистрация', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user: User = auth_srv.get_user_by_email(form.email.data)
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/tasks")
            return render_template(prefix + '/login.html', message="Неправильный логин или пароль", form=form)
        except UserDoesNotExistError:
            return render_template(prefix + '/login.html', message="Неправильный логин или пароль", form=form)
    return render_template(prefix + '/login.html', title='Авторизация', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/profile')
def profile():
    if current_user.is_authenticated:
        with db_session.create_session() as session:
            tasks: list[Task] = session.query(Task).where(current_user.id == Task.creator_id).all()
            statuses: list[Status] = session.query(Status).all()
            tasks_count: dict[str, int] = {status.name: 0 for status in statuses}
            for task in tasks:
                tasks_count[task.status.name] += 1
        return render_template(prefix + '/profile.html', tasks_count=tasks_count)
    return redirect('/')


@blueprint.route('/profile/edit')
@login_required
def edit_profile():
    return render_template(prefix + '/profile.html')


@blueprint.route('/yandex-login')
def yandex_login():
    """Reginster or sign in by means of Yandex Account."""
    redirect_url = YANDEX_API_REQUEST
    return redirect(redirect_url)


@blueprint.route('/yandex-callback')
def yandex_callback():
    """Fetch a response from Yandex."""
    code = request.args.get('code')
    if code:
        token_url = 'https://oauth.yandex.ru/token'
        token_params = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': YA_CLIENT_ID,
            'client_secret': YA_CLIENT_SECRET
        }
        response = requests.post(token_url, data=token_params)
        data = response.json()
        if 'access_token' in data:
            user_info_url = 'https://login.yandex.ru/info'
            headers = {'Authorization': f'OAuth {data['access_token']}'}
            user_info_response = requests.post(user_info_url, headers=headers)
            user_info = user_info_response.json()
            print(user_info)
            username = user_info.get('login')
            email = user_info.get('default_email')
            social_uid = str(user_info.get('id'))
            print(current_user)
            if current_user.is_authenticated and current_user.oauth_yandex_id is None:
                auth_srv.add_yandex_oauth_id(current_user.id, social_uid)
            elif not current_user.is_authenticated:
                auth_srv.login_by_yandex_id(social_uid)
    return redirect('/')