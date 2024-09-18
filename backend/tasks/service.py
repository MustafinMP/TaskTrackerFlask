from datetime import datetime

from flask_login import current_user
from sqlalchemy import select, and_, delete, update
from sqlalchemy.orm import joinedload

import db_session
from tasks.models import Status, Task, Tag
from teams.models import Team, user_to_team


def select_all_statuses() -> list[Status, ...]:
    """Find all task statuses in database

    :return: list of status objects.
    """

    with db_session.create_session() as session:
        stmt = select(Status)
        return session.scalars(stmt).all()


def create_task(name: str, description: str, deadline: datetime | None = None, status_id: int | None = None) -> None:
    """Create new task and save it to database.

    :param name: the task name (task header).
    :param description: the task description.
    :param deadline: datetime, when task should be done.
    :param status_id: the id of task status.
    :return: no return.
    """

    with db_session.create_session() as session:
        task = Task()
        task.name = name
        task.description = description
        task.team_id = current_user.current_team_id
        if deadline is not None:
            task.deadline = deadline
        if status_id is not None:
            task.status_id = status_id
        session.add(task)
        session.commit()


def select_task_by_status(status_id: int) -> list[Task, ...]:
    """Find tasks by their status.

    :param status_id: the id of task status.
    :return: list of tasks with current status.
    """

    stmt = select(Task).where(
        Task.status_id == status_id
    ).join(Task.team).filter(
        Team.id == current_user.current_team_id
    )
    with db_session.create_session() as session:
        return session.scalars(stmt).all()


def select_task_by_id(task_id: int) -> Task | None:
    """Find task by id.

    :param task_id: the id of task.
    :return: task object or none.
    """

    stmt = select(Task).where(
        Task.id == task_id
    ).join(Task.team).filter(
        Team.id == current_user.current_team_id
    ).options(
        joinedload(Task.creator)
    )
    with db_session.create_session() as session:
        return session.scalar(stmt)


def select_task_by_team_id(team_id: int) -> list[Task, ...]:
    stmt = select(Task).join(Task.team).filter(
        Team.id == team_id
    ).options(
        joinedload(Task.creator)
    )
    with db_session.create_session() as session:
        return session.scalars(stmt)


def update_task_status(task_id: int, new_status_id: int) -> None:
    """Update status of current task.

    :param task_id: the id of task.
    :param new_status_id: the id of new status.
    :return: no return.
    """

    stmt = update(Task).where(
        and_(
            Task.id == task_id,
            Task.team_id == user_to_team.c.team,
            user_to_team.c.team == current_user.current_team_id
        )
    ).values(status_id=new_status_id)
    with db_session.create_session() as session:
        session.execute(stmt)
        session.commit()


def update_task(task_id: int, new_name: str, new_description: str, new_status_id: int) -> None:
    """Update information about current task.

    :param task_id: the id of task.
    :param new_name: the new name of task.
    :param new_description: the new description of task.
    :param new_status_id: the id of new status.
    :return: no return.
    """

    stmt = update(Task).where(
        and_(
            Task.id == task_id,
            Task.team_id == user_to_team.c.team,
            user_to_team.c.team == current_user.current_team_id
        )
    ).values(
        name=new_name,
        description=new_description,
        status_id=new_status_id
    )
    with db_session.create_session() as session:
        session.execute(stmt)
        session.commit()


def delete_task(task_id: int) -> None:
    """Delete the task from database by id.

    :param task_id: the id of the task.
    :return: no return.
    """

    stmt = delete(Task).where(
        and_(
            Task.id == task_id,
            Task.team_id == user_to_team.c.team,
            user_to_team.c.team == current_user.current_team_id
        )
    )
    with db_session.create_session() as session:
        session.execute(stmt)
        session.commit()


def add_tag_to_task(task_id: int, tag_id: int) -> None:
    """Add tag to task.

    :param task_id: the id of the task.
    :param tag_id: the id of the tag.
    :return: no return.
    """

    task_stmt = select(Task).where(
        Task.id == task_id
    ).join(Task.team).filter(
        Team.id == current_user.current_team
    )
    tag_stmt = select(Tag).where(
            Tag.id == tag_id
        )
    with db_session.create_session() as session:
        task: Task = session.scalar(task_stmt)
        tag: Tag = session.scalar(tag_stmt)
        tag.tasks.append(task)
        session.commit()
