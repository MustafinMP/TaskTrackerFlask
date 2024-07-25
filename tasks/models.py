from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, orm
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    creator_id: int = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_date: datetime = Column(TIMESTAMP, default=datetime.now)
    status_id: int = Column(Integer, ForeignKey('status.id'), default=0, nullable=False)

    creator = orm.relationship('User', foreign_keys=[creator_id])
    status = orm.relationship('Status', foreign_keys=[status_id])


class Status(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'status'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(length=50), nullable=False)