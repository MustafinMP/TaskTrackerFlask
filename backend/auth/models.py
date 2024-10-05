from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


from db_session import SqlAlchemyBase
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Main user model.

    :param id: the unique user identification key.
    :param name: just the username.
    :param email: the email of the user.
    :param hashed_password: the hash of user password.
    :param created_date: the date, when ...
    :param image: the filename of user profile image.
    :param current_team_id: the id of last current team.
    :param current_team: the last current team.
    """

    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=True)
    email: str = Column(String, index=True, unique=True, nullable=True)
    hashed_password: str = Column(String, nullable=True)
    created_date: datetime = Column(TIMESTAMP, default=datetime.now)
    image: str = Column(String, nullable=True, default='default.png')
    current_team_id: int = Column(Integer, ForeignKey('team.id'), nullable=True)

    current_team = relationship('Team', foreign_keys=[current_team_id], lazy="joined")
    teams = relationship('Team', secondary='user_to_team', back_populates='members', lazy="joined")

    def set_password(self, password: str) -> None:
        """Create hash of user password and save it.

        :param password: no hashed password.
        :return: no return.
        """
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check that the user password is valid.

        :param password: no hashed password.
        :return: result of checking.
        """
        return check_password_hash(self.hashed_password, password)
