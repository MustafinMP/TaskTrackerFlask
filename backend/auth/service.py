import os

from sqlalchemy import select
from werkzeug.utils import secure_filename

import db_session
from auth.forms import RegisterForm
from auth.models import User
from teams.service import create_team


def save_file(file) -> str:
    filename = secure_filename(file.filename)
    file.save(os.path.join('../static/uploads', filename))
    return filename


def select_user_by_email(user_email):
    with db_session.create_session() as session:
        stmt = select(User).where(User.email == user_email)
        return session.scalar(stmt)


def user_exists_by_email(user_email):
    return select_user_by_email(user_email) is not None


def create_user(form: RegisterForm):
    user = User()
    user.name = form.name.data
    user.email = form.email.data
    user.set_password(form.password.data)
    save_file(form.image.data)
    create_team(user.id, team_name=f"Personal {user.name}'s team")
    with db_session.create_session() as session:
        session.add(user)
