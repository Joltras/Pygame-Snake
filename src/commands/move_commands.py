from src.elements.actor.actor import Actor
from src.commands.command import Command


class MoveUpCommand(Command):

    def execute(self, actor: Actor):
        return actor.move_up()


class MoveDownCommand(Command):

    def execute(self, actor: Actor):
        return actor.move_down()


class MoveLeftCommand(Command):

    def execute(self, actor: Actor):
        return actor.move_left()


class MoveRightCommand(Command):

    def execute(self, actor: Actor):
        return actor.move_right()
