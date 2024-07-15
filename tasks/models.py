from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey

from db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'task'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    creator: int = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_date: datetime = Column(TIMESTAMP, default=datetime.now)
    status: int = Column(Integer, ForeignKey('status.id'), default=0, nullable=False)


class Status(SqlAlchemyBase):
    __tablename__ = 'status'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(length=50), nullable=False)