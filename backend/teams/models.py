from sqlalchemy import Integer, Column, String, ForeignKey

from db_session import SqlAlchemyBase


class Team(SqlAlchemyBase):
    __tablename__ = 'team'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)


class Role(SqlAlchemyBase):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    team: int = Column(Integer, ForeignKey('team.id'))
    user: int = Column(Integer, ForeignKey('user.id'))


class Permission(SqlAlchemyBase):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
