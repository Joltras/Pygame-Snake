import unittest

from src.utils.direction import Direction


class DirectionTest(unittest.TestCase):
    def test_opposite(self):
        self.assertEqual(Direction.DOWN, Direction.UP.opposite())
        self.assertEqual(Direction.UP, Direction.DOWN.opposite())
        self.assertEqual(Direction.RIGHT, Direction.LEFT.opposite())
        self.assertEqual(Direction.LEFT, Direction.RIGHT.opposite())


if __name__ == '__main__':
    unittest.main()
