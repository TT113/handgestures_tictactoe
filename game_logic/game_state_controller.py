from model.player import Player


class GameStateController:
    def __init__(self, state):
        self.state = state
        self.width = len(state.field)
        self.height = len(state.field[0])

    def get_cell(self, coordinate):
        if not self.validate_position(coordinate):
            raise Exception("Invalid coordinate")

        return self.state.field[coordinate.x][coordinate.y]

    def set_cell(self, coordinate, cell_occupation):
        if not self.validate_position(coordinate):
            raise Exception("Invalid coordinate")

        self.state.field[coordinate.x][coordinate.y] = cell_occupation

    def next_player(self):
        if self.state.turn == Player.X:
            self.state.turn = Player.O
        else:
            self.state.turn = Player.X

    def validate_position(self, coordinate):
        if coordinate.x < 0 or coordinate.x >= self.width:
            return False

        if coordinate.y < 0 or coordinate.y >= self.height:
            return False

        return True