from enum import Enum


class GameState(Enum):
    STARTING = 0
    RUNNING = 1
    WON = 2
    GAME_OVER = 3
    CLOSE_GAME = 4
    PAUSED = 5