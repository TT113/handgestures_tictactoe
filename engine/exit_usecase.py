import pygame
from sys import exit


class DefaultPlatformExit:
    def __init__(self, camera):
        self.camera = camera

    def exit(self):
        self.camera.stop_recording()
        pygame.quit()
        exit(0)