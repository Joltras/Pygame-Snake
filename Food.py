import random
from Game_Field import GameField
from Globals import SQUARE_SIZE
from pygame import Rect


class Food:

    def __init__(self, x: int, y: int):
        """
        Creates a new food object.
        A food object is a rectangle which can be randomly placed on a field.
        :param x:
        :param y:
        """
        self.__rect = Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)

    def get_rect(self):
        """
        Returns the Rectangle of the object
        :return: Rectangle
        """
        return self.__rect

    def place(self, x: int, y: int):
        """
        Places the food-object on a random location on a field.
        :param x:
        :param y:
        """
        self.__rect = Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
