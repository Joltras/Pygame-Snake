from typing import List

import pygame

from src.elements.game_element import GameElement
from src.utils.color import Color
from src.utils.globals import SQUARE_SIZE
from pygame import Rect


class Food(GameElement):

    def __init__(self, x: int, y: int, top: int, left: int):
        """
        Creates a new food object at the given coordinates
        :param x: x-coordinate
        :param y: y-coordinate
        """
        self._rect = Rect(x * SQUARE_SIZE + left, y * SQUARE_SIZE + top, SQUARE_SIZE, SQUARE_SIZE)

    def collides(self, rects: List[Rect]) -> bool:
        return self._rect.collidelist(rects) != -1;

    def draw(self, screen) -> None:
        pygame.draw.rect(screen, Color.BLACK.value, self._rect)

    def get_rect(self):
        """
        Returns the Rectangle of the object
        :return: Rectangle
        """
        return self._rect

