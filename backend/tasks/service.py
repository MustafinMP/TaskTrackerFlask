from flask_login import current_user
from sqlalchemy import select, and_, delete, update
from sqlalchemy.orm import joinedload

import db_session
from tasks.models import Status, Task, Tag


def select_all_statuses() -> list[Status, ...]:
    with db_session.create_session() as session:
        stmt = select(Status)
        return session.scalars(stmt).all()


def create_task(name: str, description: str, status_id: int | None = None) -> None:
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
        stmt = select(Task).where(
            and_(
                current_user.id == Task.creator_id,
                Task.status_id == status_id
            )
        )
        return session.scalars(stmt).all()


def select_task_by_id(task_id: int) -> Task | None:
    with db_session.create_session() as session:
        stmt = select(Task).where(
            and_(
                current_user.id == Task.creator_id,
                Task.id == task_id
            )
        ).options(joinedload(Task.creator))
        return session.scalar(stmt)


def update_task_status(task_id: int, new_status_id: int) -> None:
    with db_session.create_session() as session:
        stmt = update(Task).where(
            and_(
                current_user.id == Task.creator_id,
                Task.id == task_id
            )
        ).values(status_id=new_status_id)
        session.execute(stmt)
        session.commit()


def update_task(task_id: int, new_name: str, new_description: str, new_status_id: int) -> None:
    with db_session.create_session() as session:
        stmt = update(Task).where(
            and_(
                current_user.id == Task.creator_id,
                Task.id == task_id
            )
        ).values(
            name=new_name,
            description=new_description,
            status_id=new_status_id
        )
        session.execute(stmt)
        session.commit()


def delete_task(task_id: int) -> None:
    with db_session.create_session() as session:
        stmt = delete(Task).where(
            and_(
                current_user.id == Task.creator_id,
                Task.id == task_id
            )
        )
        session.execute(stmt)
        session.commit()


def add_tag_to_task(task_id: int, tag_id: int) -> None:
    with db_session.create_session() as session:
        stmt_task = select(Task).where(
            and_(
                current_user.id == Task.creator_id,
                Task.id == task_id
            )
        )
        task: Task = session.scalar(stmt_task)
        stmt_tag = select(Tag).where(
            Tag.id == tag_id
        )
        tag: Tag = session.scalar(stmt_tag)
        tag.tasks.append(task)
        session.commit()
