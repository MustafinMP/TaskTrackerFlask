from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, orm
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


color_tags: tuple[str] = tuple(
    [
        'grey',
        'red',
        'orange',
        'green',
    ]
)


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task'
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    creator_id: int = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    created_date: datetime = Column(TIMESTAMP, default=datetime.now)
    status_id: int = Column(Integer, ForeignKey('status.id'), default=0, nullable=False)

    creator = orm.relationship('User', foreign_keys=[creator_id])
    status = orm.relationship('Status', foreign_keys=[status_id])


class Status(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'status'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(length=50), nullable=False)
    color_tag: str = Column(String(length=30), nullable=True, default=color_tags[0])

    @validates('color_tag')
    def validate_color_tag(self, key, value):
        if value not in color_tags:
            raise ValueError("Color tag doesn't exist")
        return value


