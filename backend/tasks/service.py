from datetime import datetime

from flask_login import current_user

import db_session
from tasks.exceptions import TaskDoesNotExistError, UserPermissionError
from tasks.models import Status, Task
from tasks.repository import TaskRepository, StatusRepository
from teams.service import user_in_team_by_ids


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


def get_tasks_by_statuses(team_id: int, statuses: list[Status]) -> dict[int, list[Task]]:
    with db_session.create_session() as session:
        repository = TaskRepository(session)
        tasks = {
            status.id: repository.get_by_status(status.id, team_id)
            for status in statuses
        }
        return tasks


def get_task_by_id(task_id: int) -> Task:
    """Find task by id.

    :param task_id: the id of task.
    :return: task object or none.
    """

    with db_session.create_session() as session:
        repository = TaskRepository(session)
        task = repository.get_by_id(task_id)
        if not task:
            raise TaskDoesNotExistError
        if not user_in_team_by_ids(current_user.id, task.team.id):
            raise UserPermissionError
        return task


def update_task(task_id: int, new_name: str = None, new_description: str = None, new_status_id: int = None) -> None:
    """Update information about current task.

    :param task_id: the id of task.
    :param new_name: the new name of task.
    :param new_description: the new description of task.
    :param new_status_id: the id of new status.
    :return: no return.
    """

    with db_session.create_session() as session:
        repository = TaskRepository(session)
        task = repository.get_by_id(task_id)
        if not task:
            raise TaskDoesNotExistError
        if not user_in_team_by_ids(current_user.id, task.team.id):
            raise UserPermissionError
        repository.update_object(
            task,
            new_name=new_name,
            new_description=new_description,
            new_status_id=new_status_id
        )


def delete_task(task_id: int) -> None:
    with db_session.create_session() as session:
        repository = TaskRepository(session)
        task: Task = repository.get_by_id(task_id)
        if not task:
            raise TaskDoesNotExistError
        if current_user not in task.team.members:
            raise UserPermissionError
        repository.delete_object(task)


def get_statuses() -> list[Status]:
    with db_session.create_session() as session:
        repository = StatusRepository(session)
        return repository.get_all()
