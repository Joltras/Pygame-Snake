from collections import deque

from pygame import Rect
from src.Globals import SQUARE_SIZE

from src.actor.Actor import Actor


class Snake(Actor):

    def __init__(self, x: int, y: int, top: int, left: int):
        """
        Creates a new snake object with the given arguments.
        :param x: x-coordinate
        :param y: y-coordinate
        """
        self.__segments = deque()
        self.__segments.append(Rect(x * SQUARE_SIZE + left, y * SQUARE_SIZE + top, SQUARE_SIZE, SQUARE_SIZE))
        self.__last_segment = None

    def get_head(self) -> Rect:
        """
        Returns the first segment of the snake.
        :return: first segment
        """
        return self.__segments[0]

    def get_length(self):
        return len(self.__segments)

    def collides_with_body(self, rect: Rect) -> bool:
        """
        Checks if the segments of the snake collide with a given rectangle.
        :param rect: Rectangle to check collision
        :return: True when they collide otherwise False
        """
        if rect.collidelist(self.__segments) != -1:
            return True
        else:
            return False

    def collides_with_itself(self) -> bool:
        """
        Checks if the segments of the snake collide with each other.
        :return: True if they collide otherwise False
        """
        segm = self.__segments.copy()
        segm.popleft()
        if self.__segments[0].collidelist(segm) != -1:
            return True
        else:
            return False

    def collides_with_head(self, rect: Rect) -> bool:
        if rect.colliderect(self.__segments[0]):
            return True
        return False

    def __add_and_remove_last(self, new_head):
        self.__segments.appendleft(new_head)
        self.__last_segment = self.__segments.pop()

    def move_up(self):
        old_head = self.__segments[0]
        new_head = old_head.move(0, -SQUARE_SIZE)
        self.__add_and_remove_last(new_head)

    def move_down(self):
        old_head = self.__segments[0]
        new_head = old_head.move(0, SQUARE_SIZE)
        self.__add_and_remove_last(new_head)

    def move_left(self):
        old_head = self.__segments[0]
        new_head = old_head.move(-SQUARE_SIZE, 0)
        self.__add_and_remove_last(new_head)

    def move_right(self):
        old_head = self.__segments[0]
        new_head = old_head.move(SQUARE_SIZE, 0)
        self.__add_and_remove_last(new_head)

    def grow(self):
        self.__segments.append(self.__last_segment)

    def get_segments(self):
        return self.__segments
