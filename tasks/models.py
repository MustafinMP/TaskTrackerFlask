from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey

from db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'task'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    creator: int = Column(Integer, ForeignKey('user.id'))
    created_date: datetime = Column(TIMESTAMP, default=datetime.now)
    is_closed: bool = Column(Boolean, default=False, nullable=False)