from game_logic.game_state_controller import GameFieldController
from model.cell_occupation import CellOccupation
from model.winner import Winner


class TicTacToeDefaultWinnerCheckStrategy:
    def check(self, field):
        board_controller = GameFieldController(field)
        if board_controller.height != 3 or board_controller.width != 3:
            return Winner.NONE

        line_check_results = []
        for i in range(board_controller.height):
            line_check_result = TicTacToeDefaultWinnerCheckStrategy.check_line(board_controller.field[i])
            line_check_results.append(line_check_result)

        diagonal_top_right = [board_controller.field[i][board_controller.height-1-i] for i in range(board_controller.height)]
        line_check_results.append(TicTacToeDefaultWinnerCheckStrategy.check_line(diagonal_top_right))

        diagonal_top_left = [board_controller.field[i][i] for i in range(board_controller.height)]
        line_check_results.append(TicTacToeDefaultWinnerCheckStrategy.check_line(diagonal_top_left))

        for i in range(board_controller.height):
            line = []
            for j in range(board_controller.width):
                line.append(board_controller.field[j][i])
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
