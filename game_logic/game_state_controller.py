from model.cell_occupation import CellOccupation
from model.player import Player


class GameFieldController:
    def __init__(self, field):
        self.width = len(field)
        self.height = len(field[0])
        self.field = field

    def get_cell(self, coordinate):
        if not self.validate_position(coordinate):
            return CellOccupation.INVALID_CELL

        return self.field[coordinate.y][coordinate.x]

    def set_cell(self, coordinate, cell_occupation):
        if not self.validate_position(coordinate):
            return

        self.field[coordinate.y][coordinate.x] = cell_occupation

    def validate_position(self, coordinate):
        if coordinate.x < 0 or coordinate.x >= self.width:
            return False

        if coordinate.y < 0 or coordinate.y >= self.height:
            return False

        return True
