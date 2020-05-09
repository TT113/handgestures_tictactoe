import threading

import pygame

from display.engine import TickGenerator, TickSplitter
from display.system_time_frame_update_strategy import SystemTimeFrameUpdateStrategy
from display.tictactoedefault33scene import TicTacToeDefault33Scene
from model.input import Input
from model.player import Player
from renderers.pygame_renderer import PyGameRenderer
from renderers.text_renderer import TextRenderer
import time
import keyboard


from utils.PublishSubject import Subject


class InputterX:
    def __init__(self, scene):
        self.actions = [Input.ENTER, Input.BOTTOM_ARROW, Input.ENTER, Input.BOTTOM_ARROW, Input.ENTER]
        self.scene = scene
        self.current_action = 0

    def update(self, scene):
        print("receive state update", scene.game_state.turn, scene.cursor_position)
        if self.current_action < len(self.actions) and scene.game_state.turn == Player.X:
            current_action = self.actions[self.current_action]
            self.current_action += 1
            print("give_input", current_action)
            self.scene.receive_input(current_action)


class InputterO:
    def __init__(self, scene):
        self.actions = [Input.RIGHT_ARROW, Input.ENTER, Input.RIGHT_ARROW, Input.ENTER]
        self.scene = scene
        self.current_action = 0

    def update(self, scene):
        if self.current_action < len(self.actions) and scene.game_state.turn == Player.O:
            current_action = self.actions[self.current_action]
            self.current_action += 1
            self.scene.receive_input(current_action)


class SceneUpdateWrapper:
    def __init__(self, update_lambda):
        self.update_lambda = update_lambda

    def update(self, game_state):
        print("receive frame update")
        self.update_lambda(game_state)


class Executor:
    def __init__(self, executed_fn):
        self.executed_fn = executed_fn

    def tick(self):
        self.executed_fn()


class KeyboardInputUpdater:
    def __init__(self, scene):
        self.scene = scene
        pygame.init()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # As long as an arrow key is held down, the respective speed is set to 3 (or minus 3)
                if event.key == pygame.K_LEFT:
                    scene.receive_input(Input.LEFT_ARROW)
                elif event.key == pygame.K_RIGHT:
                    scene.receive_input(Input.RIGHT_ARROW)
                elif event.key == pygame.K_UP:
                    scene.receive_input(Input.TOP_ARROW)
                elif event.key == pygame.K_DOWN:
                    scene.receive_input(Input.BOTTOM_ARROW)
                elif event.key == pygame.K_SPACE:
                    scene.receive_input(Input.ENTER)


scene_state_subject = Subject()
scene = TicTacToeDefault33Scene(scene_state_subject.update_subject)

scene_state_subject._subject_state = scene.get_render_model()
renderer = PyGameRenderer()
renderer.setup_with_field(scene.get_render_model().game_state)
tick_generator = TickGenerator(60)
tick_generator.add_subscriber(KeyboardInputUpdater(scene))
tick_generator.add_subscriber(Executor(lambda: renderer.render(scene.get_render_model())))

# render on scene state change
# scene_state_subject.attach(SceneUpdateWrapper(lambda x: renderer.render(x)), True)
scene_state_subject.attach(InputterX(scene), True)
# scene_state_subject.attach(InputterO(scene), True)
input_x, input_o = scene.get_input_controllers()
# input_x(Input.ENTER)
# input_o(Input.ENTER)


tick_generator.run_ticks()

