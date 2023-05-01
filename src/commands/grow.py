from src.actor.actor import Actor
from src.commands.command import Command


class GrowCommand(Command):
    def execute(self, actor: Actor):
        actor.grow()
