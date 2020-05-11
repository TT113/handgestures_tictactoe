from game_logic.game_state_controller import GameFieldController
from model.cell_occupation import CellOccupation
from model.move_result import MoveResult
from model.player import Player
from model.winner import Winner


class TicTacToeGame:
    def __init__(self, state, finish_strategy, state_callback):
        self.state = state
        self.controller = GameFieldController(state.field)
        self.game_is_ongoing = True
        self.winner = None
        self.turn = Player.X
        self.finish_strategy = finish_strategy
        self.state_callback = state_callback

    def __make_move(self, coordinate):
        current_cell_state = self.controller.get_cell(coordinate)

        if current_cell_state != CellOccupation.FREE:
            return MoveResult.CELL_OCCUPIED

        if not self.game_is_ongoing:
            return MoveResult.GAME_NOT_STARTED

        # make move as for current player
        new_cell_state = CellOccupation.X
        if self.state.turn == Player.O:
            new_cell_state = CellOccupation.O
        self.controller.set_cell(coordinate, new_cell_state)

        # check if current move finished game
        winner = self.finish_strategy.check(self.state.field)
        if winner != Winner.NONE:
            self.game_is_ongoing = False
            self.winner = winner
            return MoveResult.GAME_FINISHED

        if self.controller.is_board_fully_occupied():
            self.game_is_ongoing = False
            return  MoveResult.GAME_FINISHED

        self.__next_move()

        return MoveResult.OK

    def make_move(self, coordinate):
        move_result = self.__make_move(coordinate)
        self.state_callback(self.state)
        return move_result

    def __next_move(self):
        if self.state.turn == Player.X:
            self.state.turn = Player.O
        else:
            self.state.turn = Player.X
