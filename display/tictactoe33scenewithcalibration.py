from display.tictactoedefault33scene import *
import time


class TicTacToe33SceneWithController(TicTacToeDefault33Scene):
    def __init__(self, game_changed_callback):
        TicTacToeDefault33Scene.__init__(self, game_changed_callback)
        self.cv_input_controller = None
        self.cv_controller_calibrated = False

    def before_get_render_model(self):
        if time.time() - self.game_begin_timestamp > 20 and not self.cv_controller_calibrated and self.cv_input_controller is not None:
            self.cv_controller_calibrated = True
            self.cv_input_controller.calibrate()

    def set_cv_controller(self, cv_controller):
        self.cv_input_controller = cv_controller
