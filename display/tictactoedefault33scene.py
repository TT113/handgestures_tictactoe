from game_logic.tic_tac_toe_default_winner_check_strategy import TicTacToeDefaultWinnerCheckStrategy
from game_logic.tictactoe_game import TicTacToeGame
from game_logic.user_cursor_controller import UserCursorController
from model.game_state import GameState
from model.input import Input
from model.move_result import MoveResult
from model.scene_render_model import SceneModel


# class InputReceiver:
#     def __init__(self):
#         self.input_command = Input.NO_INPUT
#
#     def set_input(self, input):
#         self.input_command = input
#
#     def get_input(self):
#         current_input = self.input_command
#         self.input_command = Input.NO_INPUT
#         return current_input

class TicTacToeDefault33Scene:

    def __init__(self, game_changed_callback):
        game_state = GameState.get_default_with_field(3,3)
        self.game = TicTacToeGame(game_state, TicTacToeDefaultWinnerCheckStrategy(), self.game_changed_callback)
        self.user_cursor_controller = UserCursorController(game_state)
        self.scene_changed_callback = game_changed_callback

    def receive_input(self, input):
        if input == Input.BOTTOM_ARROW:
            self.user_cursor_controller.input_arrow_down()
        if input == Input.LEFT_ARROW:
            self.user_cursor_controller.input_arrow_left()
        if input == Input.RIGHT_ARROW:
            self.user_cursor_controller.input_arrow_right()
        if input == Input.TOP_ARROW:
            self.user_cursor_controller.input_arrow_up()

        if input == Input.ENTER:
            self.game.make_move(self.user_cursor_controller.cursor_position)
        else:
            self.game_changed_callback(self.game.state)

    def game_changed_callback(self, game_state):
        self.scene_changed_callback(SceneModel(game_state, self.user_cursor_controller.cursor_position))

    def get_render_model(self):
        return SceneModel(self.game.state, self.user_cursor_controller.cursor_position)