import unittest

from pygame import Rect

from src.elements.food import Food
from src.utils.globals import SQUARE_SIZE


class FoodTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__food = Food(3, 4, 0, 0)
        self.__food_offset = Food(3, 4, 50, 40)

    def test_rect(self):
        expected = Rect(3 * SQUARE_SIZE, 4 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        self.assertEqual(expected, self.__food.get_rect())

    def test_rect_offset(self):
        expected = Rect(3 * SQUARE_SIZE + 40, 4 * SQUARE_SIZE + 50, SQUARE_SIZE, SQUARE_SIZE)
        self.assertEqual(expected, self.__food_offset.get_rect())

    def test_collides_true(self):
        rect = Rect(3 * SQUARE_SIZE, 4 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        self.assertTrue(self.__food.collides([rect]))

    def test_collides_false(self):
        rect = Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE)
        self.assertFalse(self.__food.collides([rect]))

    def test_collides_empty_list(self):
        self.assertFalse(self.__food.collides([]))


if __name__ == '__main__':
    unittest.main()
