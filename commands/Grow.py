from actor.Actor import Actor
from commands.Command import Command


class GrowCommand(Command):
    def execute(self, actor: Actor):
        actor.grow()
