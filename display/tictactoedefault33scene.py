from game_logic.tic_tac_toe_default_winner_check_strategy import TicTacToeDefaultWinnerCheckStrategy
from game_logic.tictactoe_game import TicTacToeGame
from game_logic.user_cursor_controller import UserCursorController
from model.game_state import GameState
from model.input import Input
from model.move_result import MoveResult
from model.scene_render_model import SceneRenderModel


class TicTacToeDefault33Scene:

    def __init__(self):
        game_state = GameState(3, 3)
        self.game = TicTacToeGame(game_state, TicTacToeDefaultWinnerCheckStrategy())
        self.last_move_result = MoveResult.GAME_NOT_STARTED
        self.user_cursor_controller = UserCursorController(game_state)

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
            self.last_move_result = self.game.make_move(self.user_cursor_controller.cursor_position)

    def get_render_model(self):
        return SceneRenderModel(self.game.controller.state, self.user_cursor_controller.cursor_position, self.last_move_result)