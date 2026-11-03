import unittest

import pygame
from pygame import Rect, Surface

from src.elements.game_field import GameField
from src.ui.buttons.button.text_button import TextButton
from src.ui.message import MessageDisplayer, BUTTON_GAP

WIDTH = 600
HEIGHT = 450


class MessageDisplayerTest(unittest.TestCase):
    def setUp(self) -> None:
        pygame.font.init()
        self.__screen = Surface((WIDTH, HEIGHT))
        self.__field = GameField(WIDTH, HEIGHT)
        self.__displayer = MessageDisplayer(WIDTH, HEIGHT, 0, 0)
        self.__button1 = TextButton(Rect(0, 0, 120, 40), "Start", lambda: None)
        self.__button2 = TextButton(Rect(0, 0, 100, 30), "Exit", lambda: None)
        self.__displayer.create_message(self.__field, "Title", self.__screen, self.__button1, self.__button2)

    def test_buttons_centered_horizontally(self):
        left = self.__button1._rect.left
        right = self.__button2._rect.right
        self.assertEqual(WIDTH // 2, (left + right) // 2)

    def test_buttons_gap(self):
        self.assertEqual(BUTTON_GAP, self.__button2._rect.left - self.__button1._rect.right)

    def test_buttons_same_vertical_center(self):
        self.assertEqual(self.__button1._rect.centery, self.__button2._rect.centery)

    def test_buttons_below_title(self):
        self.assertGreater(self.__button1._rect.top, HEIGHT // 2)


if __name__ == '__main__':
    unittest.main()
