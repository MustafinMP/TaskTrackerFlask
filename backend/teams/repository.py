from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from auth.models import User
from auth.repository import UserRepository
from teams.models import Team, user_to_team


class TeamRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, creator_id: int, team_name: str = None) -> None:
        """Create new team and save it to database.

    :param creator_id: the id of the user creating the team.
    :param team_name: the name of new team.
    :return: no return.
    """

        new_team = Team()
        new_team.creator_id = creator_id
        if team_name is None:
            team_name = 'New team'
        new_team.name = team_name
        self.session.add(new_team)
        self.session.commit()

    def add_new_members(self, team_id: int, *new_member_ids: list[int]) -> None:
        """

        :param team_id: the id of the current team.
        :param new_member_ids: the list of ids of new team members.
        :return: no return.
        """

        team = self.get_by_id(team_id)
        user_repository = UserRepository(self.session)
        for new_member_id in new_member_ids:
            member = user_repository.get_by_id(new_member_id)
            if member is not None:
                team.members.append(member)
                self.session.add(team)
        self.session.commit()

    def get_by_id(self, team_id: int) -> Team:
        stmt = select(Team).where(Team.id == team_id)
        return self.session.scalar(stmt)

    def get_by_member_id(self, member_id: int) -> list[Team]:
        teams_stmt = select(Team).join(Team.members).filter(User.id == member_id)
        teams = self.session.scalars(teams_stmt).unique().fetchall()
        return teams

    def have_member_by_ids(self, user_id: int, team_id: int) -> bool:
        stmt = select(user_to_team).where(
            and_(
                user_to_team.c.user == user_id,
                user_to_team.c.team == team_id,
            )
        )
        return self.session.scalar(stmt) is not None
