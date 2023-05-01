import pygame
from pygame import Rect

from src.elements.game_element import GameElement
from src.utils.color import Color


class PlayingArea(GameElement):

    def __init__(self, width: int, height: int, left: int = 0, top: int = 0):
        self._width = width
        self._height = height
        self._field_rect = Rect(left, top, self._width, self._height)

    def draw(self, screen) -> None:
        pygame.draw.rect(screen, Color.LIGHT_GRAY.value, self._field_rect)

    def collides(self, rects) -> bool:
        return False
