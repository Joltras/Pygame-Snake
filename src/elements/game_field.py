import random
from overrides import override
from src.elements.game_border import GameBorder
from src.elements.game_element import GameElement
from src.elements.playing_area import PlayingArea
from src.utils.globals import SQUARE_SIZE
from typing import List


class GameField(GameElement):

    def __init__(self, width, height, left: int = 0, top: int = 0):
        """
        Creates a new GameField with the given data.
        :param width: width of the game field in pixel
        :param height: height of the game field in pixel
        :param left: left offset for the game field in pixel (default = 0)
        :param top: top offset for the game field in pixel
        """
        self._width_in_squares = width // SQUARE_SIZE
        self._width = width

        self._height_in_squares = height // SQUARE_SIZE
        self._height = height

        self._left = left
        self._top = top

        self._elements: List[GameElement] = [PlayingArea(width=self._width, height=self._height),
                                             GameBorder(width_in_squares=self._width_in_squares, height_in_squares=self._height_in_squares)]

        # Create the border of the field
    def get_top(self) -> int:
        return self._top

    def get_left(self) -> int:
        return self._left

    def get_width(self) -> int:
        """
        Returns the width of the field.
        :return: width
        """
        return self._width

    def get_width_in_squares(self) -> int:
        """
        Returns how many squares can fit in a row of the field.
        :return: number of squares
        """
        return self._width_in_squares

    def get_height(self) -> int:
        """
        Returns the height of the field.
        :return: height
        """
        return self._height

    def get_height_in_squares(self):
        """
        Returns how many squares can fit in a column of the field.
        :return: number of squares
        """
        return self._height_in_squares

    @override
    def collides(self, rects) -> bool:
        """
        Checks if a rectangle collides with the border.
        :param rects: lists of rectangles
        :return: True if they collide otherwise False
        """
        return self._elements[1].collides(rects=rects)

    def random_x_on_field(self) -> int:
        """
        Calculates a random x-coordinate on the field.
        :return: coordinate
        """
        cord = random.randint(1, (self._width_in_squares - 2))
        return cord

    def random_y_on_field(self) -> int:
        """
        Calculates a random y-coordinate on the field.
        :return: coordinate
        """
        cord = random.randint(1, (self._height_in_squares - 2))
        return cord

    @override
    def draw(self, screen) -> None:
        for element in self._elements:
            element.draw(screen)
