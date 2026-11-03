import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
from pygame import Rect

from src.elements.actor.snake_actor import Snake
from src.elements.food import Food
from src.game import Game
from src.utils.game_state import GameState
from src.utils.globals import SQUARE_SIZE


def press(*keys: int) -> None:
    for key in keys:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))


def square(x: int, y: int) -> Rect:
    return Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)


class GameDirectionTest(unittest.TestCase):
    def setUp(self) -> None:
        pygame.init()
        self.__game = Game(1280, 720)
        self.__game._food = Food(1, 1, 0, 0)
        pygame.event.clear()
        # Snake with three segments at (7, 5), (6, 5), (5, 5) moving right
        snake = Snake(4, 5, 0, 0)
        for _ in range(2):
            snake.move_right()
            snake.grow()
        snake.move_right()
        self.__game._actor = snake
        self.__game._command = self.__game.move_right
        self.__game.set_running()

    def tearDown(self) -> None:
        pygame.quit()

    def __tick(self) -> None:
        self.__game._running()

    def test_reverse_is_ignored(self):
        press(pygame.K_LEFT)
        self.__tick()
        self.assertEqual(square(8, 5), self.__game._actor.get_head())
        self.assertEqual(GameState.RUNNING, self.__game._game_state)

    def test_turn(self):
        press(pygame.K_UP)
        self.__tick()
        self.assertEqual(square(7, 4), self.__game._actor.get_head())

    def test_reverse_with_two_keys_in_one_tick_is_ignored(self):
        press(pygame.K_UP, pygame.K_LEFT)
        self.__tick()
        self.assertEqual(square(7, 4), self.__game._actor.get_head())
        self.assertEqual(GameState.RUNNING, self.__game._game_state)

    def test_reverse_after_turn(self):
        press(pygame.K_UP)
        self.__tick()
        press(pygame.K_LEFT)
        self.__tick()
        self.assertEqual(square(6, 4), self.__game._actor.get_head())


if __name__ == '__main__':
    unittest.main()
