import pygame
from engine.tick_generator import RunLoop, RunLoopMember
from renderers.pygame_renderer import PyGameRenderer
from game_logic.ai_player import *
from ai.minimax_strategy import *
from engine.publishsubject import PublishSubject, PublishReceiver
from renderers.resource_loader import ResourceLoader
from scene.tictactoedefault33scene import *
from cv.nn_input import *
from engine.camera_frame_updater import CameraFrameUpdater, CameraFrameUpdaterWithDebugBlending
from cv.camera_frame_receiver import *
from engine.exit_usecase import DefaultPlatformExit
from engine.peripheral_input_controller import PeripheralInputReceiver
from engine.executor import Executor
from cv.cv_input_controller import CvInputConroller
from scene.tip_state_switch_strategy import *


def assemble_and_run_target(name):
    # shared tick generator
    tick_generator = RunLoop(120)

    # same frame update subject for both targets
    frame_update_subject = PublishSubject(tick_generator)
    camera_frame_receiver = CameraFrameReceiver(frame_update_subject.update_subject)
    camera_frame_receiver.start()

    exit_usecase = DefaultPlatformExit(camera_frame_receiver.camera)

    # scene initialization
    scene_state_subject = PublishSubject(tick_generator)
    if name == 'cv':
        tip_strategy = ShowUIStrategyFromData([
            UITimingEntry(0, 20, UIState.INITIAL_TIP),
            UITimingEntry(20, 30, UIState.CALIBRATION)
        ])
    if name == 'nn':
        tip_strategy = ShowUIStrategyFromData([
            UITimingEntry(0, 20, UIState.INITIAL_TIP),
        ])
    scene = TicTacToeDefault33Scene(scene_state_subject.update_subject, exit_usecase, tip_strategy)
    scene_state_subject._subject_state = scene.get_render_model()

    # renderer and resource loader
    if name == 'cv':
        loader = ResourceLoader.with_default_params()
    if name == 'nn':
        loader = ResourceLoader.with_nn_params()
    renderer = PyGameRenderer(loader)
    renderer.setup_with_field(scene.get_render_model().game_state)

    tick_generator.add_subscriber(camera_frame_receiver)
    tick_generator.add_subscriber(Executor(lambda: renderer.render(scene.get_render_model())))

    if name == 'cv':
        cv_input = CvInputConroller(scene, 1, loader)
        tick_generator.schedule_delayed_callback(30, lambda: cv_input.calibrate())
        tick_generator.add_subscriber(CameraFrameUpdaterWithDebugBlending(camera_frame_receiver, renderer, cv_input))

    if name == 'nn':
        cv_input = NNInputController(scene, loader)
        tick_generator.add_subscriber(CameraFrameUpdater(camera_frame_receiver, renderer))

    # attach frame updates to cv_input
    frame_update_subject.attach(PublishReceiver(lambda x: cv_input.process_frame(x)))

    # lifecycle setup
    tick_generator.add_subscriber(PeripheralInputReceiver(scene, cv_input))

    # ai player setup
    instant_input_o = scene.create_instant_move_controller(Player.O)
    ai_player = AiPlayer(instant_input_o, MinimaxStrategy(TicTacToeDefaultWinnerCheckStrategy(), Player.O), Player.O)
    scene_state_subject.attach(ai_player, True)

    tick_generator.run_ticks()


""" specify model target ("nn" - neural network, "cv" - background subtraction model)"""
assemble_and_run_target('cv')


























