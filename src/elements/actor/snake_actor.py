from collections import deque

import pygame
from overrides import override
from pygame import Rect

from src.elements.actor.actor import Actor
from src.elements.game_element import GameElement
from src.utils.color import Color
from src.utils.globals import SQUARE_SIZE


class Snake(Actor, GameElement):

    def __init__(self, x: int, y: int, top: int, left: int):
        """
        Creates a new snake object with the given arguments.
        :param x: x-coordinate
        :param y: y-coordinate
        :param top: top offset
        :param left: left offset
        """
        self._segments = deque()
        self._segments.append(Rect(x * SQUARE_SIZE + left, y * SQUARE_SIZE + top, SQUARE_SIZE, SQUARE_SIZE))
        self.__last_segment = None

    def get_head(self) -> Rect:
        """
        Returns the first segment of the snake.
        :return: first segment
        """
        return self._segments[0]

    def get_length(self):
        return len(self._segments)

    def collides(self, rects) -> bool:
        """
        Checks if the segments of the snake collide with a given rectangle.
        :param rects: Rectangles to check collision
        :return: True when they collide otherwise False
        """
        for rect in rects:
            if rect.collidelist(self._segments) != -1:
                return True
        return False

    def collides_with_itself(self) -> bool:
        """
        Checks if the segments of the snake collide with each other.
        :return: True if they collide otherwise False
        """
        head = self._segments.popleft()
        collides = self.collides([head])
        self._segments.appendleft(head)
        return collides

    def _add_and_remove_last(self, new_head):
        self._segments.appendleft(new_head)
        self.__last_segment = self._segments.pop()

    def move_up(self):
        old_head = self._segments[0]
        new_head = old_head.move(0, -SQUARE_SIZE)
        self._add_and_remove_last(new_head)

    def move_down(self):
        old_head = self._segments[0]
        new_head = old_head.move(0, SQUARE_SIZE)
        self._add_and_remove_last(new_head)

    def move_left(self):
        old_head = self._segments[0]
        new_head = old_head.move(-SQUARE_SIZE, 0)
        self._add_and_remove_last(new_head)

    def move_right(self):
        old_head = self._segments[0]
        new_head = old_head.move(SQUARE_SIZE, 0)
        self._add_and_remove_last(new_head)

    def grow(self):
        self._segments.append(self.__last_segment)

    def get_segments(self):
        return self._segments

    @override
    def draw(self, screen):
        for rect in self._segments:
            pygame.draw.rect(screen, Color.GREEN.value, rect)
            pygame.draw.rect(screen, Color.DARK_GREEN.value, rect, 2, 1)
