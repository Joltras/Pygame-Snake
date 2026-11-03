import unittest

from pygame import Rect

from src.elements.game_border import GameBorder
from src.utils.globals import SQUARE_SIZE

WIDTH_IN_SQUARES = 5
HEIGHT_IN_SQUARES = 4


def square(x: int, y: int, left: int = 0, top: int = 0) -> Rect:
    return Rect(x * SQUARE_SIZE + left, y * SQUARE_SIZE + top, SQUARE_SIZE, SQUARE_SIZE)


class GameBorderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__border = GameBorder(height_in_squares=HEIGHT_IN_SQUARES, width_in_squares=WIDTH_IN_SQUARES)
        self.__border_offset = GameBorder(height_in_squares=HEIGHT_IN_SQUARES, width_in_squares=WIDTH_IN_SQUARES,
                                          left=40, top=50)

    def test_collides_corners(self):
        for x, y in [(0, 0), (WIDTH_IN_SQUARES - 1, 0), (0, HEIGHT_IN_SQUARES - 1),
                     (WIDTH_IN_SQUARES - 1, HEIGHT_IN_SQUARES - 1)]:
            with self.subTest(x=x, y=y):
                self.assertTrue(self.__border.collides([square(x, y)]))

    def test_collides_top_and_bottom(self):
        for x in range(WIDTH_IN_SQUARES):
            with self.subTest(x=x):
                self.assertTrue(self.__border.collides([square(x, 0)]))
                self.assertTrue(self.__border.collides([square(x, HEIGHT_IN_SQUARES - 1)]))

    def test_collides_left_and_right(self):
        for y in range(HEIGHT_IN_SQUARES):
            with self.subTest(y=y):
                self.assertTrue(self.__border.collides([square(0, y)]))
                self.assertTrue(self.__border.collides([square(WIDTH_IN_SQUARES - 1, y)]))

    def test_collides_inside_false(self):
        for x in range(1, WIDTH_IN_SQUARES - 1):
            for y in range(1, HEIGHT_IN_SQUARES - 1):
                with self.subTest(x=x, y=y):
                    self.assertFalse(self.__border.collides([square(x, y)]))

    def test_collides_one_of_many(self):
        self.assertTrue(self.__border.collides([square(1, 1), square(0, 1)]))

    def test_collides_offset(self):
        self.assertTrue(self.__border_offset.collides([square(0, 0, 40, 50)]))
        self.assertFalse(self.__border_offset.collides([square(1, 1, 40, 50)]))


if __name__ == '__main__':
    unittest.main()
