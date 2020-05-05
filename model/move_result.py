from enum import Enum


class MoveResult(Enum):
    OK = 0
    CELL_OCCUPIED = 1
    GAME_NOT_STARTED = 2
    GAME_FINISHED = 3