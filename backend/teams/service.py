import db_session
from teams.models import Team
from teams.repository import TeamRepository


def add_team(creator_id: int, team_name: str = None) -> None:
    """Create new team and save it to database.

    :param creator_id: the id of the user creating the team.
    :param team_name: the name of new team.
    :return: no return.
    """

    with db_session.create_session() as session:
        repository = TeamRepository(session)
        repository.add(creator_id, team_name)
        repository.add_new_members(creator_id)


def add_new_team_members(team_id: int, *new_member_ids: list[int]) -> None:
    """Create new team and save it to database.

    :param team_id: the id of the current team.
    :param new_member_ids: the list of ids of new team members.
    :return: no return.
    """

    with db_session.create_session() as session:
        repository = TeamRepository(session)
        repository.add_new_members(team_id, *new_member_ids)


def get_user_teams_by_id(user_id: int) -> list[Team, ...]:
    with db_session.create_session() as session:
        repository = TeamRepository(session)
        return repository.get_by_member_id(user_id)


def user_in_team_by_ids(user_id: int, team_id: int) -> bool:
    with db_session.create_session() as session:
        repository = TeamRepository(session)
        repository.have_member_by_ids(user_id, team_id)


def get_team_by_id(team_id: int) -> Team:
    with db_session.create_session() as session:
        repository = TeamRepository(session)
        return repository.get_by_id(team_id)


# def get_team_data_by_id(team_id: int) -> dict:
#     stmt = select(Team).where(
#         Team.id == team_id
#     ).join(Team.members).where(
#         User.id == current_user.id
#     )
#     with db_session.create_session() as session:
#         team = session.scalar(stmt)
#         return team.to_dict(
#             only=(
#                 'name',
#                 'creator.id',
#                 'creator.name',
#                 'members.id',
#                 'members.name'
#             )
#         )