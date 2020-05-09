import os

from model.cell_occupation import CellOccupation


class TextRenderer:

    def setup_with_field(self, state):
        pass


    def render(self, model):
        os.system("clear")
        state = model.game_state

        for i in range(state.size_x):
            field_row = []
            for j in range(state.size_y):
                if state.field[i][j] == CellOccupation.X:
                    field_row.append('X')
                if state.field[i][j] == CellOccupation.O:
                    field_row.append('O')
                if state.field[i][j] == CellOccupation.FREE:
                    field_row.append('-')
            print(field_row)

        print('cursor: ' + str(model.cursor_position))
        print('last move result: ' + str(state.last_move_result))