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


class GameRestartTest(unittest.TestCase):
    def setUp(self) -> None:
        pygame.init()
        self.__game = Game(1280, 720)
        pygame.event.clear()
        # Long snake moving right that has just lost
        snake = Snake(4, 5, 0, 0)
        for _ in range(3):
            snake.move_right()
            snake.grow()
        self.__game._actor = snake
        self.__game._food = Food(1, 1, 0, 0)
        self.__game._command = self.__game.move_right
        self.__game._game_state = GameState.GAME_OVER

    def tearDown(self) -> None:
        pygame.quit()

    def __assert_reset(self) -> None:
        self.assertEqual(GameState.STARTING, self.__game._game_state)
        self.assertIsNone(self.__game._command)
        self.assertEqual(1, self.__game._actor.get_length())
        self.assertFalse(self.__game._actor.collides([self.__game._food.get_rect()]))

    def test_restart(self):
        self.__game.restart()
        self.__assert_reset()

    def test_restart_with_key(self):
        press(pygame.K_y)
        self.__game._losing()
        self.__assert_reset()

    def test_restart_with_button(self):
        # Draw the message once so the button knows its position
        self.__game._losing()
        position = self.__game._restart_button._rect.center
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=position, button=1))
        self.__game._losing()
        self.__assert_reset()

    def test_restart_does_not_keep_moving(self):
        self.__game.restart()
        self.__game.set_running()
        head = self.__game._actor.get_head().copy()
        self.__game._running()
        self.assertEqual(head, self.__game._actor.get_head())

    def test_exit_with_key(self):
        press(pygame.K_n)
        self.__game._losing()
        self.assertEqual(GameState.CLOSE_GAME, self.__game._game_state)


class GameScoreTest(unittest.TestCase):
    def setUp(self) -> None:
        pygame.init()
        self.__game = Game(1280, 720)
        pygame.event.clear()
        top = self.__game._field.get_top()
        self.__game._actor = Snake(5, 5, top, 0)
        self.__game._food = Food(6, 5, top, 0)
        self.__game._command = self.__game.move_right
        self.__game.set_running()

    def tearDown(self) -> None:
        pygame.quit()

    def test_score_starts_at_zero(self):
        self.assertEqual(0, Game(1280, 720)._score)

    def test_eating_increases_score(self):
        self.__game._running()
        self.assertEqual(1, self.__game._score)

    def test_moving_keeps_score(self):
        self.__game._food = Food(20, 10, self.__game._field.get_top(), 0)
        self.__game._running()
        self.assertEqual(0, self.__game._score)

    def test_restart_resets_score(self):
        self.__game._running()
        self.__game.restart()
        self.assertEqual(0, self.__game._score)

    def test_field_below_score_bar(self):
        self.assertEqual(self.__game._score_bar.get_height(), self.__game._field.get_top())
        self.assertEqual(720, self.__game._field.get_top() + self.__game._field.get_height())

    def test_snake_and_food_not_in_score_bar(self):
        bar_height = self.__game._score_bar.get_height()
        for _ in range(50):
            self.__game.restart()
            self.assertGreaterEqual(self.__game._actor.get_head().top, bar_height)
            self.assertGreaterEqual(self.__game._food.get_rect().top, bar_height)
