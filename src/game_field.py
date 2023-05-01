import random

from pygame import Rect
from src.utils.globals import SQUARE_SIZE


class GameField:
    width_in_squares: int
    height_in_squares: int
    x: int
    y: int
    border: list

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
        self._field_rect = Rect(left, top, self._width, self._height)

        # Create the border of the field
        self.__border = []
        y_cord = 0
        while y_cord < self._height_in_squares:
            if y_cord == 0 or y_cord == self._height_in_squares - 1:
                # Top and bottom of the field
                x_cord = 0
                while x_cord < self._width_in_squares:
                    self.__border.append(
                        Rect(x_cord * SQUARE_SIZE + left, y_cord * SQUARE_SIZE + top, SQUARE_SIZE, SQUARE_SIZE))
                    x_cord += 1
            else:
                self.__border.append(Rect(left, y_cord * SQUARE_SIZE + top, SQUARE_SIZE, SQUARE_SIZE))
                self.__border.append(
                    Rect((self._width_in_squares * SQUARE_SIZE) - SQUARE_SIZE + left, y_cord * SQUARE_SIZE + top, SQUARE_SIZE,
                         SQUARE_SIZE))
            y_cord += 1

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

    def get_border(self) -> list:
        """
        Returns the border of the field as a list of rectangles.
        :return: Border of the field
        """
        return self.__border

    def get_rect(self):
        return self._field_rect

    def collides_with_boarder(self, rects) -> bool:
        """
        Checks if a rectangle collides with the border.
        :param rects: lists of rectangles
        :return: True if they collide otherwise False
        """
        for rect in rects:
            if rect.collidelist(self.__border) != -1:
                return True
        return False

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
