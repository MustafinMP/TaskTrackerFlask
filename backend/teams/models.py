from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, Table, Column, Integer, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin

from auth.models import User
from db_session import SqlAlchemyBase

user_to_team = Table(
    'user_to_team', SqlAlchemyBase.metadata,
    Column('user', Integer, ForeignKey('user.id')),
    Column('team', Integer, ForeignKey('team.id'))
)


class Team(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    members: Mapped[List['User']] = relationship(secondary=user_to_team, back_populates='teams', lazy="joined")
    creator = relationship('User', foreign_keys=[creator_id], lazy="joined")

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


class InviteLink(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'invite_link'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(nullable=False)
    burn_datetime: Mapped[datetime] = mapped_column(TIMESTAMP)
    key: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
