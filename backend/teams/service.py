from flask_login import current_user
from sqlalchemy import select, and_, update

import db_session
from auth.models import User
from teams.models import Team, user_to_team


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
        teams = session.scalars(teams_stmt).unique().fetchall()
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


def get_team_data_by_id(team_id: int) -> dict:
    stmt = select(Team).where(
        Team.id == team_id
    ).join(Team.members).where(
        User.id == current_user.id
    )
    with db_session.create_session() as session:
        team = session.scalar(stmt)
        return team.to_dict(
            only=(
                'name',
                'creator.id',
                'creator.name',
                'members.id',
                'members.name'
            )
        )