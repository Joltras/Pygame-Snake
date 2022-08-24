import random
from Game_Field import GameField

from pygame import Rect


class Food:

    def __init__(self, field: GameField):
        """
        Creates a new food object.
        A food object is a rectangle which can be randomly placed on a field.
        :param field: Object of the game field
        """
        self.__rect = Rect(0, 0, field.get_square_size(), field.get_square_size())

    def get_rect(self):
        """
        Returns the Rectangle of the object
        :return: Rectangle
        """
        return self.__rect

    def place(self, field: GameField):
        """
        Places the food-object on a random location on a field.
        :param field: Field object
        """
        size: int = field.get_square_size()

        left = random.randint(1, (field.get_width_in_squares() - 2))
        top = random.randint(1,  (field.get_height_in_squares() - 2))
        self.__rect = Rect(left * size, top * size, size, size)

