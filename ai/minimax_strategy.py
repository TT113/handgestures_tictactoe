from game_logic.game_state_controller import *
from model.coordinate import *
from model.winner import *
from collections import namedtuple
from model.player import Player

MinimaxResult = namedtuple('MinimaxResult', ['score', 'coordinate'])


class MinimaxStrategy:
    def __init__(self, winner_check_strategy, ai_player):
        self.winner_check_strategy = winner_check_strategy
        self.ai_player = ai_player
        if ai_player == Player.X:
            self.opponent_player = Player.O
        else:
            self.opponent_player = Player.X
        self.cache = {}

    def __put_cached(self, hash, move_result):
        self.cache[hash] = move_result

    def __acquire_by_hash(self, hash):
        if hash in self.cache:
            return self.cache[hash]
        return None

    def get_best_move(self, game_state):
        result = self.__minimax(game_state.field, game_state.turn, 0)
        return result.coordinate

    def __player_to_cell_occupation(self, player):
        if player == Player.X:
            return CellOccupation.X
        else:
            return CellOccupation.O

    def __winner_to_player(self, winner):
        if winner == Winner.X:
            return Player.X
        if winner == Winner.O:
            return Player.O
        return None

    def __minimax(self, field, current_player, depth):
        board_controller = GameFieldController(field)
        cached_result = self.__acquire_by_hash(board_controller.get_board_hash())
        if cached_result is not None:
            return cached_result

        possible_moves = []

        for i in range(board_controller.height):
            for j in range(board_controller.width):
                current_cell_state = board_controller.get_cell(Coordinate(j,i))
                if current_cell_state == CellOccupation.FREE:
                    possible_moves.append(Coordinate(j,i))

        current_winner = self.__winner_to_player(self.winner_check_strategy.check(field))

        if current_winner == self.ai_player:
            return MinimaxResult(10, None)
        elif current_winner == self.opponent_player:
            return MinimaxResult(-10, None)

        if len(possible_moves) == 0:
            return MinimaxResult(0, None)

        # speeds up further calculations.
        if len(possible_moves) == 9:
            return MinimaxResult(10, Coordinate(0,0))

        moves = []

        for move_coordinate in possible_moves:
            score = 0
            board_controller.set_cell(move_coordinate, self.__player_to_cell_occupation(current_player))
            if current_player == self.ai_player:
                score = self.__minimax(board_controller.field, self.opponent_player, depth+1).score
            else:
                a = self.__minimax(board_controller.field, self.ai_player, depth+1)
                score = a.score
            board_controller.set_cell(move_coordinate, CellOccupation.FREE)
            moves.append(MinimaxResult(score, move_coordinate))

        if current_player == self.ai_player:
            best_move = max(moves, key=lambda x: x.score)
            self.__put_cached(board_controller.get_board_hash(), best_move)
            return best_move

        best_move = min(moves, key=lambda x: x.score)
        self.__put_cached(board_controller.get_board_hash(), best_move)
        return best_move
