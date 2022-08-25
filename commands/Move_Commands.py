from actor.Actor import Actor
from commands.Command import Command


class MoveUpCommand(Command):

    def execute(self, actor: Actor):
        return Actor.move_up()


class MoveDownCommand(Command):

    def execute(self, actor: Actor):
        return Actor.move_down()


class MoveLeftCommand(Command):

    def execute(self, actor: Actor):
        return Actor.move_left()


class MoveRightCommand(Command):

    def execute(self, actor: Actor):
        return Actor.move_right()
