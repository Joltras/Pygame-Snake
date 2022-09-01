from enum import Enum

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
NUMBER_OF_SQUARES = 50
SQUARE_SIZE = 20


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Color(Enum):
    ORANGE = (255, 140, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 100, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (150, 150, 150)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (100, 100, 100)
    YELLOW = (250, 250, 55)
    VIOLET = (148, 0, 211)


FIELD_COLOR = Color.LIGHT_GRAY
BACKGROUND_COLOR = Color.DARK_GRAY


class GameState(Enum):
    STARTING = 0
    RUNNING = 1
    WON = 2
    GAME_OVER = 3
    CLOSE_GAME = 4
    PAUSED = 5
