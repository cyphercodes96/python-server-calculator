from threading import Thread, Timer
import time


class TimerPlus(Timer):
    started_at = None
    def start(self):
        self.started_at = time.time()
        Timer.start(self)
    def elapsed(self):
        return time.time() - self.started_at
    def remaining(self):
        return self.interval - self.elapsed()
