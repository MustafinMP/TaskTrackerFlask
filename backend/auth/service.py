import os

from flask_login import login_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

import db_session
from auth.exceptions import UserDoesNotExistError
from auth.forms import RegisterForm
from auth.models import User
from auth.repository import UserRepository
from auth.views import login
from teams.repository import TeamRepository
from teams.service import add_team


def save_file(file) -> str:
    print(type(file))
    filename = secure_filename(file.filename)
    file.save(os.path.join('../static/uploads', filename))
    return filename


def get_user_by_id(user_id: int) -> User | None:
    """Find user in database by id.

    :param user_id: the id of the user.
    :return: user object or none.
    """

    with db_session.create_session() as session:
        repository = UserRepository(session)
        return repository.get_by_id(user_id)


def get_user_by_email(user_email: str) -> User | None:
    """Find user in database by email.

    :param user_email: the email of the user.
    :return: user object or none.
    """

    with db_session.create_session() as session:
        repository = UserRepository(session)
        user = repository.get_by_email(user_email)
        if not user:
            raise UserDoesNotExistError
        return user


def user_exists_by_email(user_email: str) -> bool:
    """Check that user exists in database.

    :param user_email: the email of the user.
    :return: user object or none.
    """
    try:
        get_user_by_email(user_email)
        return True
    except UserDoesNotExistError:
        return False


def add_user(form: RegisterForm) -> None:
    """Create new user by data from register form.

    :param form: the valid form with register data.
    :return: no return.
    """

    save_file(form.image.data)
    with db_session.create_session() as session:
        user_repository = UserRepository(session)
        user_repository.add(
            form.name.data,
            form.email.data,
            form.password.data
        )
        user = user_repository.get_by_email(form.email.data)
        team_repository = TeamRepository(session)
        team_repository.add(user.id, team_name=f"Personal {user.name}'s team")


