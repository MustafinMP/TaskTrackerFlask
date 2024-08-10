from flask_login import current_user
from sqlalchemy import select, and_, Select

import db_session
from tasks.models import Status, Task


def stmt_task_by_id(task_id: int) -> Select:
    return select(Task).where(
        and_(
            current_user.id == Task.creator_id,
            Task.id == task_id
        )
    )


def stmt_task_by_status_id(status_id: int) -> Select:
    return select(Task).where(
        and_(
            current_user.id == Task.creator_id,
            Task.status_id == status_id
        )
    )


def select_all_statuses() -> list[Status, ...]:
    with db_session.create_session() as session:
        stmt = select(Status)
        return session.scalars(stmt).all()


def create_task(name: str, description: str, status_id=None) -> None:
    with db_session.create_session() as session:
        task = Task()
        task.name = name
        task.description = description
        task.creator_id = current_user.get_id()
        if status_id is not None:
            task.status_id = status_id
        session.add(task)
        session.commit()


def select_task_by_status(status_id: int) -> list[Task, ...]:
    with db_session.create_session() as session:
        stmt = stmt_task_by_status_id(status_id)
        return session.scalars(stmt).all()


def select_task_by_id(task_id: int) -> Task | None:
    with db_session.create_session() as session:
        stmt = stmt_task_by_id(task_id)
        return session.scalar(stmt)


def update_task_status(task_id: int, new_status_id: int) -> None:
    with db_session.create_session() as session:
        stmt = stmt_task_by_id(task_id)
        task: Task = session.scalar(stmt)
        task.status_id = new_status_id
        session.commit()


def update_task(task_id: int, new_name, new_description, new_status_id) -> None:
    with db_session.create_session() as session:
        stmt = stmt_task_by_id(task_id)
        task: Task = session.scalar(stmt)
        task.name = new_name
        task.description = new_description
        task.status_id = new_status_id
        session.commit()


def delete_task(task_id) -> None:
    with db_session.create_session() as session:
        stmt = stmt_task_by_id(task_id)
        task: Task = session.scalar(stmt)
        session.delete(task)
        session.commit()
