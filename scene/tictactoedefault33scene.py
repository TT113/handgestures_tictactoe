from game_logic.tic_tac_toe_default_winner_check_strategy import TicTacToeDefaultWinnerCheckStrategy
from game_logic.tictactoe_game import TicTacToeGame
from game_logic.user_cursor_controller import UserCursorController
from model.game_state import GameState
from model.input import Input
from model.scene_state import SceneState
from model.player import Player
from model.scene_render_model import SceneModel
from model.coordinate import Coordinate
from model.move_result import MoveResult
import time


class TicTacToeDefault33Scene:
    """Wires up tic tac toe logical state, display logical state and input."""
    def __init__(self, game_changed_callback, exit_usecase, ui_show_strategy):
        game_state = GameState.get_default_with_field(3, 3)
        self.scene_changed_callback = game_changed_callback
        self.ui_show_strategy = ui_show_strategy
        self.game = TicTacToeGame(game_state, TicTacToeDefaultWinnerCheckStrategy(), self.game_changed_callback)
        self.user_cursor_controller = UserCursorController(game_state)
        self.exit_usecase = exit_usecase
        self.game_begin_timestamp = time.time()
        self.game_finished_timestamp = None

    def new_init(self):
        self.game_finished_timestamp = None
        game_state = GameState.get_default_with_field(3, 3)
        self.game = TicTacToeGame(game_state, TicTacToeDefaultWinnerCheckStrategy(), self.game_changed_callback)
        self.user_cursor_controller.cursor_position = Coordinate(1, 1)

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
            if self.game.game_is_ongoing:
                self.instant_move(self.user_cursor_controller.cursor_position)
            else:
                self.new_init()

        if input == Input.EXIT:
            self.exit_usecase.exit()

        self.game_changed_callback(self.game.state)

    def game_changed_callback(self, game_state):
        self.scene_changed_callback(self.get_render_model())

    def get_render_model(self):
        self.before_get_render_model()
        return SceneModel(self.game.state, SceneState(self.user_cursor_controller.cursor_position,
                                                      self.ui_show_strategy.get_ui_state(time.time() - self.game_begin_timestamp),
                                                      self.game_begin_timestamp,
                                                      self.game.winner))

    def __create_filtered_controller(self, player):
        def controller(input):
            if self.game.state.turn == player:
                self.receive_input(input)
        return controller

    def create_instant_move_controller(self, player):
        def controller(input_coordinate):
            if self.game.state.turn == player:
                self.instant_move(input_coordinate)
        return controller

    def get_input_controllers(self):
        return self.__create_filtered_controller(Player.X), self.__create_filtered_controller(Player.O)

    def instant_move(self, coordinate):
        if self.game.make_move(coordinate) == MoveResult.GAME_FINISHED:
            self.game_finished_timestamp = time.time()

    def before_get_render_model(self):
        if self.game_finished_timestamp is not None \
                and time.time() - self.game_finished_timestamp > 20 \
                and not self.game.game_is_ongoing:
            self.exit_usecase.exit()
        pass

