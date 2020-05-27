from engine.tick_generator import RunLoopMember
import pygame
from model.input import *


class PeripheralInputReceiver(RunLoopMember):
    def __init__(self, scene, cv_input):
        RunLoopMember.__init__(self)
        self.scene = scene
        self.cv_input = cv_input
        pygame.init()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.scene.receive_input(Input.LEFT_ARROW)
                elif event.key == pygame.K_RIGHT:
                    self.scene.receive_input(Input.RIGHT_ARROW)
                elif event.key == pygame.K_UP:
                    self.scene.receive_input(Input.TOP_ARROW)
                elif event.key == pygame.K_DOWN:
                    self.scene.receive_input(Input.BOTTOM_ARROW)
                elif event.key == pygame.K_SPACE:
                    self.scene.receive_input(Input.ENTER)
                elif event.key == pygame.K_b:
                    self.cv_input.calibrate()
            elif event.type == pygame.QUIT:
                self.scene.receive_input(Input.EXIT)