import pytest
from sqlalchemy import select

from auth.models import User
from tasks.repository import TaskRepository
from tests.conftest import create_task_statuses, create_user_and_team, create_test_session


def test_add_task_1(session):
    user_stmt = select(User).where(User.email == 'test@mail.ru').unique()
    user: User = session.scalar(user_stmt)
    repository = TaskRepository(session)
    repository.add(user.id, user.current_team_id, 'First test', 'First test task')
    tasks = repository.get_by_team_id(0)
    assert tasks[0].name == 'First test'
