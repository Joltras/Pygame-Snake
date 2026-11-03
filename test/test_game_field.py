import unittest

from pygame import Rect

from src.elements.game_field import GameField
from src.utils.globals import SQUARE_SIZE

WIDTH_IN_SQUARES = 10
HEIGHT_IN_SQUARES = 8


class GameFieldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__field = GameField(WIDTH_IN_SQUARES * SQUARE_SIZE + 5, HEIGHT_IN_SQUARES * SQUARE_SIZE + 5)

    def test_width_in_squares(self):
        self.assertEqual(WIDTH_IN_SQUARES, self.__field.get_width_in_squares())

    def test_height_in_squares(self):
        self.assertEqual(HEIGHT_IN_SQUARES, self.__field.get_height_in_squares())

    def test_collides_with_border(self):
        self.assertTrue(self.__field.collides([Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE)]))

    def test_collides_inside_false(self):
        rect = Rect(SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        self.assertFalse(self.__field.collides([rect]))

    def test_random_x_not_on_border(self):
        for _ in range(200):
            self.assertIn(self.__field.random_x_on_field(), range(1, WIDTH_IN_SQUARES - 1))

    def test_random_y_not_on_border(self):
        for _ in range(200):
            self.assertIn(self.__field.random_y_on_field(), range(1, HEIGHT_IN_SQUARES - 1))


if __name__ == '__main__':
    unittest.main()
