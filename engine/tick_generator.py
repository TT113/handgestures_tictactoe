import time


class TickGenerator:
    def __init__(self, frequency_hz):
        self.frequency_hz = frequency_hz
        self.subscribers = []

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def run_ticks(self):
        while True:
            timestamp = time.time()
            timestamp_should_end_tick = timestamp + 1 / self.frequency_hz

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

