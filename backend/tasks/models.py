from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, orm, Table
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase

color_tags: tuple[str] = tuple(
    [
        'primary',
        'danger',
        'warning',
        'success',
        'light'
    ]
)


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task'
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    creator_id: int = Column(Integer, ForeignKey('user.id'), nullable=True, index=True)
    created_date: datetime = Column(TIMESTAMP, default=datetime.now)
    deadline: datetime = Column(TIMESTAMP, nullable=True)
    status_id: int = Column(Integer, ForeignKey('status.id'), default=0, nullable=False)
    team_id: int = Column(Integer, ForeignKey('team.id'), nullable=True)

    creator = orm.relationship('User', foreign_keys=[creator_id], lazy="joined")
    status = orm.relationship('Status', foreign_keys=[status_id], lazy="joined")
    team = orm.relationship('Team', foreign_keys=[team_id], backref='tasks', lazy="joined")


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


class Tag(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tag'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(length=50), nullable=False)
    tasks = orm.relationship('Task', secondary='task_to_tag', backref='tags', lazy="joined")


task_to_tag = Table(
    'task_to_tag', SqlAlchemyBase.metadata,
    Column('task', Integer, ForeignKey('task.id')),
    Column('tag', Integer, ForeignKey('tag.id'))
)
