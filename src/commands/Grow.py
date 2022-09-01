from src.actor.Actor import Actor
from src.commands.Command import Command


class GrowCommand(Command):
    def execute(self, actor: Actor):
        actor.grow()
