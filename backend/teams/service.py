from sqlalchemy import select

import db_session
from auth.models import User
from teams.models import Team


def create_team(creator_id: int, team_name: str = None) -> None:
    """Create new team and save it to database.

    :param creator_id: the id of the user creating the team.
    :param team_name: the name of new team. Defaults to ``'127.0.0.1'``
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
    """

    with db_session.create_session() as session:
        stmt = select(Team).where(Team.id == team_id)
        team = session.scalar(stmt)

        for new_member_id in new_member_ids:
            member_stmt = select(User).where(User.id == new_member_id)
            if (member := session.scalar(member_stmt)) is not None:
                team.members.append(member)
