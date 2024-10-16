from typing import Callable

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session, declarative_base
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_NAME_TEST, \
    DB_PORT_TEST

SqlAlchemyBase = declarative_base()

__factory: Callable = None
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def global_init() -> None:
    """Init a database session factory.

    :return: no return.
    """

    global __factory

    if __factory:
        return

    print(f"Подключение к базе данных {DB_NAME}")

    engine = sa.create_engine(DATABASE_URL, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from auth.models import User
    from tasks.models import Task, Status, task_to_tag
    from teams.models import Team, user_to_team
    from timer.models import TimerDelta
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """Return a new database session.

    :return: new database session object.
    """

    global __factory
    return __factory()

