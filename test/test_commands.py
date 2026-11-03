import unittest

from src.commands.grow import GrowCommand
from src.commands.move_commands import MoveUpCommand, MoveDownCommand, MoveLeftCommand, MoveRightCommand
from src.elements.actor.actor import Actor


class RecordingActor(Actor):
    def __init__(self):
        self.calls = []

    def move_up(self) -> None:
        self.calls.append("up")

    def move_down(self) -> None:
        self.calls.append("down")

    def move_left(self) -> None:
        self.calls.append("left")

    def move_right(self) -> None:
        self.calls.append("right")

    def grow(self) -> None:
        self.calls.append("grow")


class CommandsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__actor = RecordingActor()

    def test_move_up(self):
        MoveUpCommand().execute(self.__actor)
        self.assertEqual(["up"], self.__actor.calls)

    def test_move_down(self):
        MoveDownCommand().execute(self.__actor)
        self.assertEqual(["down"], self.__actor.calls)

    def test_move_left(self):
        MoveLeftCommand().execute(self.__actor)
        self.assertEqual(["left"], self.__actor.calls)

    def test_move_right(self):
        MoveRightCommand().execute(self.__actor)
        self.assertEqual(["right"], self.__actor.calls)

    def test_grow(self):
        GrowCommand().execute(self.__actor)
        self.assertEqual(["grow"], self.__actor.calls)


if __name__ == '__main__':
    unittest.main()
