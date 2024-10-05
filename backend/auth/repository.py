from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from auth.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        """Find user in database by id.

        :param user_id: the id of the user.
        :return: user object or none.
        """

        stmt = select(User).where(User.id == user_id).options(joinedload(User.teams))
        return self.session.scalar(stmt)

    def get_by_email(self, user_email: str) -> User | None:
        """Find user in database by email.

        :param user_email: the email of the user.
        :return: user object or none.
        """

        stmt = select(User).where(User.email == user_email)
        return self.session.scalar(stmt)

    def add(self, name: str, email: str, password: str) -> None:
        """Create new user by data from register form.

        :param name:
        :param email:
        :param password:
        :return: no return.
        """

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        self.session.add(user)
        self.session.commit()
