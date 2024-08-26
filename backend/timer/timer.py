import threading
from datetime import datetime, timedelta
from time import sleep


class Timer:
    def __init__(self):
        self._time = timedelta()
        self._pause = False
        self.start_datetime = datetime.now()

    def update(self):
        sleep(1)
        if not self._pause:
            self._time += timedelta(seconds=1)

    def pause(self):
        self._pause = True

    def cont(self):
        self._pause = False

    def get_time(self):
        return self._time

    def loop(self):
        while True:
            self.update()


class TimerManager:
    def __init__(self):
        self.timers = []
        self.threads = []

    def add_timer(self):
        new_timer = Timer()
        thread = threading.Thread(target=new_timer.loop, daemon=True)
        thread.start()
        self.timers.append(new_timer)
        self.threads.append(thread)

    def get_time(self, timer_id):
        return self.timers[timer_id].get_time()

    def pause(self, timer_id):
        return self.timers[timer_id].pause()

    def cont(self, timer_id):
        return self.timers[timer_id].cont()

    def terminate(self, timer_id):
        del self.threads[timer_id]
        del self.timers[timer_id]


tm = TimerManager()


def loop():
    while True:
        command = input('Do >>')
        if command == 'add':
            tm.add_timer()
            print('Timer added')
        elif command == 'get':
            timer_id = int(input('Timer num >>'))
            print(tm.get_time(timer_id))
        elif command == 'pause':
            timer_id = int(input('Timer num >>'))
            print(tm.pause(timer_id))
        elif command == 'cont':
            timer_id = int(input('Timer num >>'))
            print(tm.cont(timer_id))
        elif command == 'del':
            timer_id = int(input('Timer num >>'))
            print(tm.terminate(timer_id))


loop()