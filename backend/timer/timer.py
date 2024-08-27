import threading
from datetime import datetime, timedelta
from time import sleep

import db_session
from timer.models import TimerDelta


class Timer:
    def __init__(self, user_id, task_id):
        self._time = timedelta()
        self._pause = False
        self._pause_count = 0
        self.user_id = user_id
        self.task_id = task_id
        self.start_datetime = datetime.now()

    def update(self) -> None:
        sleep(1)
        if not self._pause:
            self._time += timedelta(seconds=1)

    def pause(self) -> None:
        if not self._pause:
            self._pause_count += 1
        self._pause = True

    def cont(self) -> None:
        self._pause = False

    def get_time(self) -> timedelta:
        return self._time

    def to_db_model(self) -> TimerDelta:
        model = TimerDelta()
        model.user_id = self.user_id
        model.task_id = self.task_id
        model.start_datetime = self.start_datetime
        model.end_datetime = datetime.now()
        model.interval = self._time
        model.pause_count = self._pause_count
        return model

    def loop(self) -> None:
        while True:
            self.update()


class TimerManager:
    def __init__(self):
        self._timers: dict[Timer] = dict()
        self._threads: dict[threading.Thread] = dict()

    def add_timer(self, user_id: int, task_id: int) -> None:
        new_timer = Timer(user_id, task_id)
        thread = threading.Thread(target=new_timer.loop, daemon=True)
        thread.start()
        self._timers[user_id] = new_timer
        self._threads[user_id] = thread

    def has_timer(self, user_id) -> bool:
        return user_id in self._timers.keys()

    def get_time(self, user_id) -> timedelta:
        return self._timers[user_id].get_time()

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

    def delete(self, user_id):
        del self._threads[user_id]
        del self._timers[user_id]
