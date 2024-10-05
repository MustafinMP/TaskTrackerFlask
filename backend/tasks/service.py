from datetime import datetime

from flask_login import current_user
from sqlalchemy import select, and_, delete, update
from sqlalchemy.orm import joinedload

import db_session
from tasks.exceptions import TaskDoesNotExistError, UserPermissionError
from tasks.models import Status, Task, Tag
from tasks.repository import TaskRepository
from teams.models import Team, user_to_team


def add_task(name: str, description: str, deadline: datetime | None = None, status_id: int | None = None) -> None:
    """Create new task and save it to database.

    :param name: the task name (task header).
    :param description: the task description.
    :param deadline: datetime, when task should be done.
    :param status_id: the id of task status.
    :return: no return.
    """
    with db_session.create_session() as session:
        repository = TaskRepository(session)
        repository.add(
            current_user.id,
            current_user.current_team_id,
            name,
            description,
            deadline,
            status_id
        )


def get_tasks_by_statuses(team_id: int) -> (list[Status, ...], dict[int, list[Task, ...]]):
    with db_session.create_session() as session:
        status_stmt = select(Status)
        statuses: list[Status, ...] = session.scalars(status_stmt).all()
        statuses.sort(key=lambda status: status.id)

        repository = TaskRepository(session)
        tasks: dict[int, list[Task, ...]] = {
            status.id: repository.get_by_status(status.id, team_id)
            for status in statuses
        }
        return statuses, tasks


def get_task_by_id(task_id: int) -> Task | None:
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


def get_task_by_id2(task_id: int) -> Task | None:
    """Find task by id.

    :param task_id: the id of task.
    :return: task object or none.
    """

    with db_session.create_session() as session:
        repository = TaskRepository(session)
        task = repository.get_by_id(task_id, current_user.current_team_id)
        if task:
            return task
        raise TaskDoesNotExistError


def update_task(task_id: int, new_name: str = None, new_description: str = None, new_status_id: int = None) -> None:
    """Update information about current task.

    :param task_id: the id of task.
    :param new_name: the new name of task.
    :param new_description: the new description of task.
    :param new_status_id: the id of new status.
    :return: no return.
    """

    values = dict()
    if new_name:
        values['name'] = new_name
    if new_description:
        values['description'] = new_description
    if new_status_id:
        values['status_id'] = new_status_id

    stmt = update(Task).where(
        and_(
            Task.id == task_id,
            Task.team_id == user_to_team.c.team,
            user_to_team.c.team == current_user.current_team_id
        )
    ).values(**values)
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


def delete_task(task_id: int) -> None:
    with db_session.create_session() as session:
        repository = TaskRepository(session)
        task: Task = repository.get_by_id(task_id)
        if not task:
            raise TaskDoesNotExistError
        if current_user not in task.team.members:
            raise UserPermissionError
        repository.delete_object(task)
