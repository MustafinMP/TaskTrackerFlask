import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

SqlAlchemyBase = dec.declarative_base()

__factory = None
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def global_init():
    global __factory

    if __factory:
        return

    print(f"Подключение к базе данных {DB_NAME}")

    engine = sa.create_engine(DATABASE_URL, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from auth.models import User
    from tasks.models import Task
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()