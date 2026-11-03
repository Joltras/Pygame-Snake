import unittest

import pygame
from pygame import Surface

from src.ui.score_bar import ScoreBar, SCORE_BAR_HEIGHT, BACKGROUND_COLOR, TEXT_COLOR

WIDTH = 400


class ScoreBarTest(unittest.TestCase):
    def setUp(self) -> None:
        pygame.font.init()
        self.__bar = ScoreBar(WIDTH)
        self.__screen = Surface((WIDTH, 300))

    def __colors_in_bar(self) -> set:
        colors = set()
        for x in range(WIDTH):
            for y in range(SCORE_BAR_HEIGHT):
                colors.add(tuple(self.__screen.get_at((x, y)))[:3])
        return colors

    def test_height(self):
        self.assertEqual(SCORE_BAR_HEIGHT, self.__bar.get_height())

    def test_draw_background(self):
        self.__bar.draw(self.__screen, 0)
        self.assertEqual(BACKGROUND_COLOR.value, tuple(self.__screen.get_at((WIDTH - 1, 0)))[:3])

    def test_draw_text(self):
        self.__bar.draw(self.__screen, 12)
        self.assertIn(TEXT_COLOR.value, self.__colors_in_bar())

    def test_draw_only_in_bar(self):
        self.__bar.draw(self.__screen, 0)
        self.assertEqual((0, 0, 0), tuple(self.__screen.get_at((0, SCORE_BAR_HEIGHT)))[:3])


if __name__ == '__main__':
    unittest.main()
