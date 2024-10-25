import pytest
from sqlalchemy import select, delete

from auth.models import User
from auth.repository import UserRepository
from tasks.repository import TaskRepository
from tests.conftest import test_session, test_engine


def test_add_user(test_session):
    user_repository = UserRepository(test_session)
    user_repository.add('Test Name', 'test@mail.ru', 'secret123')
    user: User = user_repository.get_by_email('test@mail.ru')
    assert user.name == 'Test Name'
    delete_stmt = delete(User).where(User.email == 'test@mail.ru')
    test_session.execute(delete_stmt)
    test_session.commit()


def test_add_user_with_exist_email(test_session):
    user_repository = UserRepository(test_session)
    user_repository.add('Test Name', 'test@mail.ru', 'secret123')
    try:
        user_repository.add('Test Name', 'test@mail.ru', 'secret123')
        assert False
    except Exception:
        assert True
    delete_stmt = delete(User).where(User.email == 'test@mail.ru')
    test_session.execute(delete_stmt)
    test_session.commit()


