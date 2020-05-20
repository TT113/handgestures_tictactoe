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
from cv.cv_input_controller import CvInputConroller
from game_logic.ai_player import *
from ai.minimax_strategy import *
from game_logic.tic_tac_toe_default_winner_check_strategy import TicTacToeDefaultWinnerCheckStrategy
from utils.PublishSubject import Subject
from renderers.resource_loader import ResourceLoader


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


class KeyboardInputReceiver:
    def __init__(self, scene, cv_input):
        self.scene = scene
        self.cv_input = cv_input
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
                elif event.key == pygame.K_b:
                    self.cv_input.calibrate()


class CameraFrameUpdater:
    def __init__(self, cv_engine, renderer):
        self.cv_engine = cv_engine
        self.renderer = renderer

    def tick(self):
        frame = self.cv_engine.last_processed_frame
        if frame is not None:
            self.renderer.set_camera_frame(frame)


scene_state_subject = Subject()
scene = TicTacToeDefault33Scene(scene_state_subject.update_subject)

renderer = PyGameRenderer(ResourceLoader.with_default_params())


cv_input = CvInputConroller(scene, 1)
cv_input.start()

scene_state_subject._subject_state = scene.get_render_model()




renderer.setup_with_field(scene.get_render_model().game_state)
tick_generator = TickGenerator(60)

tick_generator.add_subscriber(KeyboardInputReceiver(scene, cv_input))
tick_generator.add_subscriber(Executor(lambda: renderer.render(scene.get_render_model())))
tick_generator.add_subscriber(cv_input)
tick_generator.add_subscriber(CameraFrameUpdater(cv_input, renderer))

input_x, input_o = scene.get_input_controllers()

scene_state_subject.attach(AiPlayer(input_x, MinimaxStrategy(TicTacToeDefaultWinnerCheckStrategy(), Player.O), Player.O, scene), True)

# cv_input.calibrate()
tick_generator.run_ticks()


