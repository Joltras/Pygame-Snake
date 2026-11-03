from src.commands.command import Command
from src.elements.actor.actor import Actor
from src.utils.direction import Direction


class MoveCommand(Command):
    direction: Direction

    def is_opposite(self, command: Command) -> bool:
        """
        Checks if the given command moves in the opposite direction.
        :param command: command to compare with
        :return: True if the command moves in the opposite direction otherwise False
        """
        return isinstance(command, MoveCommand) and self.direction.opposite() == command.direction


class MoveUpCommand(MoveCommand):
    direction = Direction.UP

    def execute(self, actor: Actor):
        return actor.move_up()


class MoveDownCommand(MoveCommand):
    direction = Direction.DOWN

    def execute(self, actor: Actor):
        return actor.move_down()


class MoveLeftCommand(MoveCommand):
    direction = Direction.LEFT

    def execute(self, actor: Actor):
        return actor.move_left()


class MoveRightCommand(MoveCommand):
    direction = Direction.RIGHT

    def execute(self, actor: Actor):
        return actor.move_right()
