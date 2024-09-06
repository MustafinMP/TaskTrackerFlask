import os

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

import db_session
from auth.forms import RegisterForm
from auth.models import User
from teams.service import create_team


def save_file(file) -> str:
    print(type(file))
    filename = secure_filename(file.filename)
    file.save(os.path.join('../static/uploads', filename))
    return filename


def select_user_by_id(user_id: int) -> User | None:
    """Find user in database by id.

    :param user_id: the id of the user.
    :return: user object or none.
    """

    with db_session.create_session() as session:
        stmt = select(User).where(User.id == user_id).options(joinedload(User.teams))
        return session.scalar(stmt)


def select_user_by_email(user_email: str) -> User | None:
    """Find user in database by email.

    :param user_email: the email of the user.
    :return: user object or none.
    """

    with db_session.create_session() as session:
        stmt = select(User).where(User.email == user_email)
        return session.scalar(stmt)


def user_exists_by_email(user_email: str) -> bool:
    """Check that user exists in database.

    :param user_email: the email of the user.
    :return: user object or none.
    """

    return select_user_by_email(user_email) is not None


def create_user(form: RegisterForm) -> None:
    """Create new user by data from register form.

    :param form: the valid form with register data.
    :return: no return.
    """

    user = User()
    user.name = form.name.data
    user.email = form.email.data
    user.set_password(form.password.data)
    save_file(form.image.data)
    create_team(user.id, team_name=f"Personal {user.name}'s team")
    with db_session.create_session() as session:
        session.add(user)
