import pygame
from engine.tick_generator import RunLoop, RunLoopMember
from renderers.pygame_renderer import PyGameRenderer
from game_logic.ai_player import *
from ai.minimax_strategy import *
from engine.publishsubject import PublishSubject, PublishReceiver
from renderers.resource_loader import ResourceLoader
from scene.tictactoedefault33scene import *
from cv.nn_input import *
from cv.cv_input_controller import CvInputConroller
from engine.camera_frame_updater import CameraFrameUpdater, CameraFrameUpdaterWithDebugBlending
from cv.camera_frame_receiver import *


class Executor(RunLoopMember):
    def __init__(self, executed_fn):
        RunLoopMember.__init__(self)
        self.executed_fn = executed_fn

    def tick(self):
        self.executed_fn()


class KeyboardInputReceiver(RunLoopMember):
    def __init__(self, scene, cv_input):
        RunLoopMember.__init__(self)
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


from threading import Thread

tick_generator = RunLoop(120, "ui")
tick_generator_recognition = RunLoop(120, "calc")


def start_calculation_thread():
    print("start_another_thread")
    tick_generator_recognition.run_ticks()


thread = Thread(target=start_calculation_thread)
thread.start()

scene_state_subject = PublishSubject(tick_generator)
scene = TicTacToeDefault33Scene(scene_state_subject.update_subject)

loader = ResourceLoader.with_default_params()
renderer = PyGameRenderer(loader)


# cv_input = CvInputConroller(scene, 1, loader) #NNInputController(scene, loader)
# tick_generator.schedule_delayed_callback(10, lambda: cv_input.calibrate())

cv_input = NNInputController(scene, loader)
scene_state_subject._subject_state = scene.get_render_model()


renderer.setup_with_field(scene.get_render_model().game_state)
frame_update_subject = PublishSubject(tick_generator_recognition)
camera_frame_receiver = CameraFrameReceiver(frame_update_subject.update_subject)
camera_frame_receiver.start()

frame_update_subject.attach(PublishReceiver(lambda x: cv_input.process_frame(x)))

tick_generator.add_subscriber(KeyboardInputReceiver(scene, cv_input))
tick_generator.add_subscriber(camera_frame_receiver)
tick_generator.add_subscriber(Executor(lambda: renderer.render(scene.get_render_model())))
# tick_generator.add_subscriber(CameraFrameUpdaterWithDebugBlending(camera_frame_receiver, renderer, cv_input))
tick_generator.add_subscriber(CameraFrameUpdater(camera_frame_receiver, renderer))

instant_input_o = scene.create_instant_move_controller(Player.O)
ai_player = AiPlayer(instant_input_o, MinimaxStrategy(TicTacToeDefaultWinnerCheckStrategy(), Player.O), Player.O)

scene_state_subject.attach(ai_player, True)
tick_generator.run_ticks()


