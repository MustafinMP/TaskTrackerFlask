import threading
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from time import sleep
from math import ceil

import db_session
from timer.models import TimerDelta


@dataclass
class TimerData:
    time: timedelta
    task_id: int
    pause: bool

    def as_dict(self):
        return {key: value for key, value in asdict(self).items()}

    def to_json(self):
        return {

            'time': str(timedelta(seconds=ceil(self.time.total_seconds()))),
            'task_id': self.task_id,
            'pause': self.pause
        }


class Timer:
    def __init__(self, user_id, task_id):
        self._time = timedelta()
        self._pause = False
        self._pause_count = 0
        self.user_id = user_id
        self.task_id = task_id
        self.start_datetime = datetime.now()

    def update(self) -> None:
        if not self._pause:
            self._time += timedelta(seconds=0.1)

    def pause(self) -> None:
        if not self._pause:
            self._pause_count += 1
        self._pause = True

    def cont(self) -> None:
        self._pause = False

    def get_data(self) -> TimerData:
        return TimerData(time=self._time, task_id=self.task_id, pause=self._pause)

    def to_db_model(self) -> TimerDelta:
        model = TimerDelta()
        model.user_id = self.user_id
        model.task_id = self.task_id
        model.start_datetime = self.start_datetime
        model.end_datetime = datetime.now()
        model.interval = timedelta(seconds=ceil(self._time.total_seconds()))
        model.pause_count = self._pause_count
        return model


class TimerManager:
    def __init__(self):
        self._timers: dict[int, Timer] = dict()

    def add_timer(self, user_id: int, task_id: int) -> None:
        new_timer = Timer(user_id, task_id)
        self._timers[user_id] = new_timer

    def has_timer(self, user_id) -> bool:
        return user_id in self._timers.keys()

    def get_data(self, user_id) -> TimerData:
        return self._timers[user_id].get_data()

    def pause(self, user_id) -> None:
        return self._timers[user_id].pause()

    def cont(self, user_id):
        return self._timers[user_id].cont()

    def save_and_terminate(self, user_id) -> timedelta:
        model: TimerDelta = self._timers[user_id].to_db_model()
        interval = model.interval
        with db_session.create_session() as session:
            session.add(model)
            session.commit()
        self.delete(user_id)
        return interval

    def loop(self):
        while True:
            sleep(0.1)
            for timer in self._timers.values():
                timer.update()

    def run(self):
        thread = threading.Thread(target=self.loop, daemon=True)
        thread.start()

    def delete(self, user_id):
        del self._timers[user_id]
