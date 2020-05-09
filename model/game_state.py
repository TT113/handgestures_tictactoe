from model.move_result import MoveResult
from model.player import Player
from model.cell_occupation import CellOccupation

class GameState:
    def __init__(self, field, turn=Player.X, last_move_result=MoveResult.GAME_NOT_STARTED):
        self.field = field
        self.size_x = len(field[0])
        self.size_y = len(field)
        self.turn = turn
        self.last_move_result = last_move_result

    @staticmethod
    def create_field(size_x, size_y):
        return [[CellOccupation.FREE]*size_x for i in range(size_y)]

    @staticmethod
    def get_default_with_field(size_x, size_y):
        return GameState(GameState.create_field(size_x, size_y))

