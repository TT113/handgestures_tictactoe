from model.player import Player
from model.cell_occupation import CellOccupation

class GameState:
    def __init__(self, size_x, size_y):
        self.field = [[CellOccupation.FREE]*size_x for i in range(size_y)]
        self.size_x = size_x
        self.size_y = size_y
        self.turn = Player.X
