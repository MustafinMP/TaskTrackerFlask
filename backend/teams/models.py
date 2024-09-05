from sqlalchemy import String, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.models import User
from db_session import SqlAlchemyBase


class Team(SqlAlchemyBase):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    members: Mapped[User] = relationship('Team', secondary='user_to_team')
    creator = relationship('User', foreign_keys=[creator_id])


user_to_team = Table(
    'user_to_team', SqlAlchemyBase.metadata,
    Column('user', Integer, ForeignKey('user.id')),
    Column('team', Integer, ForeignKey('team.id'))
)

# class Role(SqlAlchemyBase):
#     id: int = Column(Integer, primary_key=True, autoincrement=True)
#     name: str = Column(String, nullable=False)
#     team: int = Column(Integer, ForeignKey('team.id'))
#     user: int = Column(Integer, ForeignKey('user.id'))
#
#
# class Permission(SqlAlchemyBase):
#     id: int = Column(Integer, primary_key=True, autoincrement=True)
#     name: str = Column(String, nullable=False)
