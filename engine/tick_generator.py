import time
from collections import namedtuple
from queue import Queue

import time


Invocation = namedtuple('Invocation', ( 'fn', 'args', 'kwargs'))


class ScheduledInvocation:
    def __init__(self, invocation, delay_seconds):
        self.invocation = invocation
        self.delay_seconds = delay_seconds
        self.started_at = time.time()

    def invoke(self):
        self.invocation.fn(*self.invocation.args, **self.invocation.kwargs)

    def timeout_wait_complete(self):
        return time.time() - (self.started_at + self.delay_seconds) >= 0


class RunLoopMember:
    def __init__(self):
        self.runloop = None


class RunLoop:
    def __init__(self, frequency_hz):
        self.frequency_hz = frequency_hz
        self.subscribers = []
        self.callback_set = []

    def add_subscriber(self, subscriber):
        subscriber.runloop = self
        self.subscribers.append(subscriber)

    def run_ticks(self):
        while True:
            timestamp = time.time()
            timestamp_should_end_tick = timestamp + 1 / self.frequency_hz

            invocations_to_remove = []
            for scheduled_invocation in self.callback_set:
                if scheduled_invocation.timeout_wait_complete():
                    scheduled_invocation.invoke()
                    invocations_to_remove.append(scheduled_invocation)

            for invoked_callback in invocations_to_remove:
                self.callback_set.remove(invoked_callback)

            """uncomment for performance check"""
            # print('begin loop')
            for subscriber in self.subscribers:
                # timestamp_begin_subscriber = time.time()
                subscriber.tick()
                # print(type(subscriber), time.time() - timestamp_begin_subscriber)
            finished_tick_timestamp = time.time()
            #
            # print('end loop', finished_tick_timestamp - timestamp)

            if finished_tick_timestamp < timestamp_should_end_tick:
                remaining_time = timestamp_should_end_tick - finished_tick_timestamp
                time.sleep(remaining_time)

    def schedule_delayed_callback(self, delay_seconds, fn, args=(), kwargs={}):
        self.callback_set.append(ScheduledInvocation(Invocation(fn, args, kwargs), delay_seconds))



