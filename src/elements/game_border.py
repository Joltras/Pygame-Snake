import pygame
from overrides import override
from pygame import Rect

from src.elements.game_element import GameElement
import numpy as np

from src.utils.color import Color
from src.utils.globals import SQUARE_SIZE


class GameBorder(GameElement):

    def __init__(self, height_in_squares: int, width_in_squares: int, left: int = 0, top: int = 0):
        self._elements = np.empty(width_in_squares * 2 + (height_in_squares * 2 - 4), dtype=Rect)
        y_cord: int = 0
        i: int = 0
        while y_cord < height_in_squares:
            if y_cord == 0 or y_cord == height_in_squares - 1:
                # Top and bottom of the field
                x_cord = 0
                while x_cord < width_in_squares:
                    self._elements[i] = Rect(x_cord * SQUARE_SIZE + left, y_cord * SQUARE_SIZE + top, SQUARE_SIZE,
                                             SQUARE_SIZE)
                    x_cord += 1
                    i += 1
            else:
                self._elements[i] = Rect(left, y_cord * SQUARE_SIZE + top, SQUARE_SIZE, SQUARE_SIZE)
                i += 1
                self._elements[i] = Rect((width_in_squares * SQUARE_SIZE) - SQUARE_SIZE + left,
                                         y_cord * SQUARE_SIZE + top, SQUARE_SIZE, SQUARE_SIZE)
                i += 1
            y_cord += 1

    @override
    def draw(self, screen) -> None:
        rect: Rect
        for rect in self._elements:
            pygame.draw.rect(surface=screen, color=Color.LIGHT_GRAY.value, rect=rect)
            pygame.draw.rect(surface=screen, color=Color.GRAY.value, rect=rect, width=2)

    @override
    def collides(self, rects) -> bool:
        for rect in rects:
            if rect.collidelist(self._elements) != -1:
                return True
        return False
