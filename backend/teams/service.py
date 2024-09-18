from datetime import datetime, timedelta
from functools import cache
from hashlib import sha256
from werkzeug.security import generate_password_hash, check_password_hash

from flask import url_for
from flask_login import current_user
from sqlalchemy import select, and_, update
from sqlalchemy.orm import joinedload

import db_session
from auth.models import User
from config import INVITE_LINK_SALT
from teams.models import Team, user_to_team, InviteLink


def create_team(creator_id: int, team_name: str = None) -> None:
    """Create new team and save it to database.

    :param creator_id: the id of the user creating the team.
    :param team_name: the name of new team. Defaults to ``'127.0.0.1'``
    :return: no return.
    """

    new_team = Team()
    new_team.creator_id = creator_id
    if team_name is None:
        team_name = 'New team'
    new_team.name = team_name
    user_stmt = select(User).where(User.id == creator_id)
    with db_session.create_session() as session:
        user = session.scalar(user_stmt)
        new_team.members.append(user)
        session.add(new_team)
        session.commit()


def add_new_team_members(team_id: int, *new_member_ids: list[int]) -> None:
    """Create new team and save it to database.

    :param team_id: the id of the current team.
    :param new_member_ids: the list of ids of new team members.
    :return: no return.
    """

    with db_session.create_session() as session:
        stmt = select(Team).where(Team.id == team_id)
        team = session.scalar(stmt)
        for new_member_id in new_member_ids:
            member_stmt = select(User).where(User.id == new_member_id)
            if (member := session.scalar(member_stmt)) is not None:
                team.members.append(member)
                session.add(team)
        session.commit()


def get_user_teams(user_id: int) -> [Team, ...]:
    with db_session.create_session() as session:
        teams_stmt = select(Team).join(Team.members).filter(User.id == user_id)
        teams = session.scalars(teams_stmt).fetchall()
        return teams


def user_in_team_by_ids(user_id: int, team_id: int) -> bool:
    stmt = select(user_to_team).where(
        and_(
            user_to_team.user == user_id,
            user_to_team.team == team_id,
        )
    )
    with db_session.create_session() as session:
        return session.scalar(stmt) is not None


def get_team_by_id(team_id: int) -> Team:
    stmt = select(Team).where(
        Team.id == team_id
    ).join(Team.members).where(
            User.id == current_user.id
    )
    with db_session.create_session() as session:
        return session.scalar(stmt)


class LinkGenerator:
    @staticmethod
    def generate_link(team_id: int):
        create_datetime = datetime.now()
        primary_key: str = LinkGenerator.generate_primary_key(team_id, create_datetime)  # отдаем пользователю
        secondary_key: str = LinkGenerator.generate_secondary_key(primary_key)  # храним у себя
        LinkGenerator.add_link_to_db(team_id, create_datetime, secondary_key)
        return f"{url_for('teams.join_team')}?team_id={team_id}&key={primary_key}"

    @staticmethod
    def add_link_to_db(team_id: int, create_datetime: datetime, secondary_key: str):
        new_link = InviteLink(
            team_id=team_id,
            burn_datetime=create_datetime + timedelta(days=2),
            key=secondary_key
        )
        # update_stmt = update(InviteLink).where(
        #     InviteLink.is_active is True
        # ).values(is_active=False)
        with db_session.create_session() as session:
            session.add(new_link)
            # session.execute(update_stmt)
            session.commit()

    @staticmethod
    def generate_primary_key(team_id: int, create_datetime: datetime) -> str:
        return generate_password_hash(f'{INVITE_LINK_SALT}{team_id}{str(create_datetime)}')

    @staticmethod
    def generate_secondary_key(primary_hash: str) -> str:
        return generate_password_hash(primary_hash)

    @staticmethod
    def check_key(team_id: int, link_key: str) -> bool:
        stmt = select(InviteLink).where(
            and_(
                InviteLink.team_id == team_id,
                InviteLink.is_active == True
            )
        )
        with db_session.create_session() as session:
            link_obj = session.scalar(stmt)
            return check_password_hash(link_obj.key, link_key)
