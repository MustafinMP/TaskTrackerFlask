import dataclasses
from typing import Callable

import pytest
from sqlalchemy import select, delete

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

# test_engine = sa.create_engine(DATABASE_URL_TEST, echo=False)
# __factory_test: Callable = orm.sessionmaker(bind=test_engine)
# SqlAlchemyBase.metadata.create_all(test_engine)


@pytest.fixture()
def test_session(test_engine) -> Session:
    """Return a new test database session.

    :return: new database session object.
    """
    factory_test: Callable = orm.sessionmaker(bind=test_engine)

    session: Session = factory_test()
    return session


@pytest.fixture(scope="function")
def test_engine():
    test_engine = sa.create_engine(DATABASE_URL_TEST, echo=False)
    #SqlAlchemyBase.metadata.drop_all(test_engine)
    SqlAlchemyBase.metadata.create_all(test_engine)
    try:
        yield test_engine
    finally:
        pass
        #SqlAlchemyBase.metadata.drop_all(test_engine, checkfirst=True)

