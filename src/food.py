from src.utils.globals import SQUARE_SIZE
from pygame import Rect


class Food:

    def __init__(self, x: int, y: int, top: int, left: int):
        """
        Creates a new food object at the given coordinates
        :param x: x-coordinate
        :param y: y-coordinate
        """
        self.__rect = Rect(x * SQUARE_SIZE + left, y * SQUARE_SIZE + top, SQUARE_SIZE, SQUARE_SIZE)

    def get_rect(self):
        """
        Returns the Rectangle of the object
        :return: Rectangle
        """
        return self.__rect

