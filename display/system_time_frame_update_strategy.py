import time
import pygame

class SystemTimeFrameUpdateStrategy:
    def __init__(self, frequency):
        self.delay = 1/frequency
    def wait(self):
        # self.clock.tick(60)
        time.sleep(self.delay)