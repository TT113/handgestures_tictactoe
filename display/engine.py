import time

from model.input import Input

class TickSplitter:
    def __init__(self, skipped_ticks, wrapped_object):
        self.current_tick = 0
        self.skipped_ticks = skipped_ticks
        self.wrapped_object = wrapped_object

    def tick(self):
        if self.current_tick == self.skipped_ticks:
            self.wrapped_object.tick()
            self.current_tick = 0
        else:
            self.current_tick += 1


import time
class TickGenerator:
    def __init__(self, frequency_hz):
        self.frequency_hz = frequency_hz
        self.subscribers = []

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def run_ticks(self):
        while True:
            for subscriber in self.subscribers:
                subscriber.tick()
            time.sleep(1/self.frequency_hz)

