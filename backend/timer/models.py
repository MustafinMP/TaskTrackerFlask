from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, DateTime, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_session import SqlAlchemyBase


class TimerDelta(SqlAlchemyBase):
    __tablename__ = 'timer_delta'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.id'), nullable=False, index=True)
    start_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    interval: Mapped[timedelta] = mapped_column(Interval, nullable=False)
    pause_count: Mapped[int] = mapped_column(default=0)

    user = relationship('User', foreign_keys=[user_id])
    task = relationship('Task', foreign_keys=[task_id])
