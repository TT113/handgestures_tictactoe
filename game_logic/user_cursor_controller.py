from model.coordinate import Coordinate


class UserCursorController:
    def __init__(self, state):
        self.cursor_position = Coordinate(1, 1)
        self.bottom_limit = state.size_y
        self.right_limit = state.size_x

    def input_arrow_up(self):
        new_position = Coordinate(self.cursor_position.x, self.cursor_position.y - 1)
        if self.__validate_cursor_position(new_position):
            self.cursor_position = new_position

    def input_arrow_right(self):
        new_position = Coordinate(self.cursor_position.x + 1, self.cursor_position.y)
        if self.__validate_cursor_position(new_position):
            self.cursor_position = new_position

    def input_arrow_left(self):
        new_position = Coordinate(self.cursor_position.x - 1, self.cursor_position.y)
        if self.__validate_cursor_position(new_position):
            self.cursor_position = new_position

    def input_arrow_down(self):
        new_position = Coordinate(self.cursor_position.x, self.cursor_position.y+1)
        if self.__validate_cursor_position(new_position):
            self.cursor_position = new_position

    def move_cursor_to(self, coordinate):
        if self.__validate_cursor_position(coordinate):
            self.cursor_position = coordinate

    def __validate_cursor_position(self, coordinate):
        if coordinate.x < 0 or coordinate.x >= self.bottom_limit:
            return False

        if coordinate.y < 0 or coordinate.y >= self.right_limit:
            return False

        return True
