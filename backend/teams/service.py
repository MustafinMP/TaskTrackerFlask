from sqlalchemy import select

import db_session
from auth.models import User
from teams.models import Team


def create_team(creator_id: int, team_name: str = None):
    new_team = Team()
    new_team.creator_id = creator_id
    if team_name is None:
        team_name = 'New team'
    new_team.name = team_name
    with db_session.create_session() as session:
        session.add(new_team)
        session.commit()


def add_new_team_members(team_id: int, *new_member_ids: list[int]) -> None:
    with db_session.create_session() as session:
        stmt = select(Team).where(Team.id == team_id)
        team = session.scalar(stmt)

        for new_member_id in new_member_ids:
            member_stmt = select(User).where(User.id == new_member_id)
            if (member := session.scalar(member_stmt)) is not None:
                team.members.append(member)
