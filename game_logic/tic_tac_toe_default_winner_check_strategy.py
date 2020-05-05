from model.cell_occupation import CellOccupation
from model.winner import Winner


class TicTacToeDefaultWinnerCheckStrategy:

    def check(self, state):
        if state is None or state.size_y != 3 or state.size_x != 3:
            return Winner.NONE

        line_check_results = []
        for i in range(state.size_y):
            line_check_result = TicTacToeDefaultWinnerCheckStrategy.check_line(state.field[i])
            line_check_results.append(line_check_result)

        diagonal_top_right = [state.field[i][state.size_y-1-i] for i in range(state.size_y)]
        line_check_results.append(TicTacToeDefaultWinnerCheckStrategy.check_line(diagonal_top_right))

        diagonal_top_left = [state.field[i][i] for i in range(state.size_y)]
        line_check_results.append(TicTacToeDefaultWinnerCheckStrategy.check_line(diagonal_top_left))

        for i in range(state.size_y):
            line = []
            for j in range(state.size_x):
                line.append(state.field[j][i])
            line_check_results.append(TicTacToeDefaultWinnerCheckStrategy.check_line(line))

        if Winner.X in line_check_results:
            return Winner.X

        if Winner.O in line_check_results:
            return Winner.O

        return Winner.NONE


    @staticmethod
    def check_line(line):
        if all(cell == CellOccupation.X for cell in line):
            return Winner.X

        if all(cell == CellOccupation.O for cell in line):
            return Winner.O

        return Winner.NONE
