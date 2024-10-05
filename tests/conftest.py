import dataclasses
from typing import Callable

import pytest
from sqlalchemy import select

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from config import DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST
from db_session import SqlAlchemyBase

from auth.models import User
from tasks.models import Task, Status, task_to_tag
from teams.models import Team, user_to_team
from timer.models import TimerDelta

DATABASE_URL_TEST = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

test_engine = sa.create_engine(DATABASE_URL_TEST, echo=False)
__factory_test: Callable = orm.sessionmaker(bind=test_engine)
SqlAlchemyBase.metadata.create_all(test_engine)


def create_test_session() -> Session:
    """Return a new test database session.

    :return: new database session object.
    """

    SqlAlchemyBase.metadata.create_all(test_engine)
    global __factory_test
    session: Session = __factory_test()
    return session


def create_task_statuses() -> None:
    for name in ['to do', 'in progress', 'done']:
        with create_test_session() as session:
            new_status = Status()
            new_status.name = name
            session.add(new_status)
            session.commit()


def create_user_and_team() -> None:
    user = User()
    user.name = 'Teas name'
    user.email = 'test@mail.ru'
    user.set_password('qwerty123')
    with create_test_session() as session:
        session.add(user)
        session.commit()
    user_stmt = select(User).where(User.email == user.email)
    with create_test_session() as session:
        user = session.scalar(user_stmt)
        new_team = Team()
        new_team.creator_id = user.id
        new_team.name = 'New team'
        new_team.members.append(user)
        session.add(new_team)
        session.commit()


@pytest.fixture(scope='session', autouse=True)
def     session() -> Session:
    SqlAlchemyBase.metadata.create_all(test_engine)
    create_task_statuses()
    create_user_and_team()
    session = create_test_session()
    yield session
    SqlAlchemyBase.metadata.drop_all(test_engine)
