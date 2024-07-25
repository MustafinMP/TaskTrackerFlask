from datetime import datetime

from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase
from sqlalchemy import Column, String, Integer, TIMESTAMP
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=True)
    email: str = Column(String, index=True, unique=True, nullable=True)
    hashed_password: str = Column(String, nullable=True)
    created_date: datetime = Column(TIMESTAMP, default=datetime.now)
    image: str = Column(String, nullable=True, default='default.png')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
