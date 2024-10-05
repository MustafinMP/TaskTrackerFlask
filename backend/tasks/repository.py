from datetime import datetime

from sqlalchemy import select, update, and_, delete
from sqlalchemy.orm import Session, joinedload

from auth.models import User
from tasks.models import Task, Tag, Status
from teams.models import Team


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(
            self,
            creator_id: int,
            team_id: int,
            name: str,
            description: str,
            deadline: datetime | None = None,
            status_id: int | None = None
    ) -> None:
        """Create new task and save it to database.

        :param team_id:
        :param creator_id:
        :param name: the task name (task header).
        :param description: the task description.
        :param deadline: datetime, when task should be done.
        :param status_id: the id of task status.
        :return: no return.
        """

        task = Task()
        task.name = name
        task.description = description
        task.team_id = team_id
        if deadline is not None:
            task.deadline = deadline
        if status_id is not None:
            task.status_id = status_id
            task.creator_id = creator_id
        self.session.add(task)
        self.session.commit()

    def add_tag_to_task(self, task_id: int, tag_id: int) -> None:
        """Add tag to task.

        :param task_id: the id of the task.
        :param tag_id: the id of the tag.
        :return: no return.
        """

        task_stmt = select(Task).where(
            Task.id == task_id
        )
        tag_stmt = select(Tag).where(
            Tag.id == tag_id
        )
        task: Task = self.session.scalar(task_stmt)
        tag: Tag = self.session.scalar(tag_stmt)
        tag.tasks.append(task)
        self.session.commit()

    def get_by_id(self, task_id: int) -> Task | None:
        """Find task by id.

        :param task_id:
        :param task_id: the id of task.
        :return: task object or none.
        """

        stmt = select(Task).where(
            Task.id == task_id
        )
        # .join(Task.team).filter(
        #     Team.id == team_id
        # ).options(
        #     joinedload(Task.creator)
        # ))
        return self.session.scalar(stmt)

    def get_by_status(self, status_id: int, team_id: int) -> list[Task, ...]:
        """Find tasks by their status.

        :param team_id: the id of team.
        :param status_id: the id of task status.
        :return: list of tasks with current status.
        """

        stmt = select(Task).where(
            Task.status_id == status_id
        ).join(Task.team).filter(
            Team.id == team_id
        )
        return self.session.scalars(stmt).unique().all()

    def get_by_team_id(self, team_id: int) -> list[Task, ...]:
        stmt = select(Task).join(Task.team).filter(
            Team.id == team_id
        ).options(
            joinedload(Task.creator)
        )
        return self.session.scalars(stmt).unique()

    def update_by_id(
            self,
            task_id: int,
            new_name: str = None,
            new_description: str = None,
            new_status_id: int = None
    ) -> None:
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
            Task.id == task_id,
        ).values(**values)
        self.session.execute(stmt)
        self.session.commit()

    def update_object(
            self,
            task: Task,
            new_name: str = None,
            new_description: str = None,
            new_status_id: int = None
    ) -> None:
        if new_name:
            task.name = new_name
        if new_description:
            task.description = new_description
        if new_status_id:
            task.status_id = new_status_id
        self.session.add(task)
        self.session.commit()

    def delete_by_id(self, task_id: int) -> None:
        """Delete the task from database by id.

        :param task_id: the id of the task.
        :return: no return.
        """

        stmt = delete(Task).where(
            Task.id == task_id
        )
        self.session.execute(stmt)
        self.session.commit()

    def delete_object(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()


class StatusRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, status_id: int) -> Status:
        stmt = select(Status).where(
            Status.id == status_id
        )
        return self.session.scalar(stmt)

    def get_all(self) -> list[Status]:
        stmt = select(Status)
        return self.session.scalars(stmt).all()


