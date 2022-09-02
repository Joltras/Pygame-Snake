import unittest
from collections import deque

from actor.Snake_Actor import Snake
from pygame import Rect
from Globals import SQUARE_SIZE


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.__snake_offset = Snake(10, 20, 50, 40)
        self.__snake_1 = Snake(10, 20, 0, 0)
        # [(300, 600)]
        self.__snake_3 = Snake(10, 20, 0, 0)
        # [(300, 540), (300, 570), (300, 600)]
        i = 0
        while i < 2:
            self.__snake_3.move_up()
            self.__snake_3.grow()
            i += 1

    def test_length(self):
        self.assertEqual(1, self.__snake_1.get_length())

    def test_snake_offset(self):
        expected = Rect(10 * SQUARE_SIZE + 40, 20 * SQUARE_SIZE + 50, SQUARE_SIZE, SQUARE_SIZE)
        self.assertEqual(expected, self.__snake_offset.get_head())

    def test_segments(self):
        expected = deque([Rect(300, 540, SQUARE_SIZE, SQUARE_SIZE), Rect(300, 570, SQUARE_SIZE, SQUARE_SIZE),
                    Rect(300, 600, SQUARE_SIZE, SQUARE_SIZE)])
        self.assertEqual(expected, self.__snake_3.get_segments())

    def test_length_3(self):
        self.assertEqual(3, self.__snake_3.get_length())

    def test_get_head(self):
        expected = Rect(10 * SQUARE_SIZE, 20 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        self.assertEqual(expected, self.__snake_1.get_head())

    def test_grow(self):
        self.__snake_1.grow()
        self.assertEqual(2, self.__snake_1.get_length())

    def test_move_up_head(self):
        expected_head = Rect(10 * SQUARE_SIZE, 20 * SQUARE_SIZE - SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        self.__snake_1.move_up()
        self.assertEqual(expected_head, self.__snake_1.get_head())

    def test_move_up_length(self):
        self.__snake_1.move_up()
        self.assertEqual(1, self.__snake_1.get_length())

    def test_move_down_head(self):
        expected_head = Rect(10 * SQUARE_SIZE, 20 * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        self.__snake_1.move_down()
        self.assertEqual(expected_head, self.__snake_1.get_head())

    def test_move_down_length(self):
        self.__snake_1.move_down()
        self.assertEqual(1, self.__snake_1.get_length())

    def test_move_left_head(self):
        expected_head = Rect(10 * SQUARE_SIZE -  SQUARE_SIZE, 20 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        self.__snake_1.move_left()
        self.assertEqual(expected_head, self.__snake_1.get_head())

    def test_move_left_length(self):
        self.__snake_1.move_left()
        self.assertEqual(1, self.__snake_1.get_length())

    def test_move_right_head(self):
        expected_head = Rect(10 * SQUARE_SIZE + SQUARE_SIZE, 20 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        self.__snake_1.move_right()
        self.assertEqual(expected_head, self.__snake_1.get_head())

    def test_move_right_length(self):
        self.__snake_1.move_right()
        self.assertEqual(1, self.__snake_1.get_length())

    def test_collides_with_body_true(self):
        rect = Rect(10 * SQUARE_SIZE, 20 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        self.assertTrue(self.__snake_1.collides_with_body(rect))

    def test_collides_with_body_false(self):
        rect = Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE)
        self.assertFalse(self.__snake_3.collides_with_body(rect))

    def test_collides_with_itself_true(self):
        self.__snake_3.move_down()
        self.assertTrue(self.__snake_3.collides_with_itself())

    def test_collides_with_itself_false(self):
        self.__snake_3.move_up()
        self.assertFalse(self.__snake_3.collides_with_itself())

    def test_collision_with_head_true(self):
        rect = Rect(300, 540, SQUARE_SIZE, SQUARE_SIZE)
        self.assertTrue(self.__snake_3.collides_with_head(rect))

    def test_collision_with_head_false(self):
        rect = Rect(300, 510, SQUARE_SIZE, SQUARE_SIZE)
        self.assertFalse(self.__snake_3.collides_with_head(rect))

if __name__ == '__main__':
    unittest.main()
