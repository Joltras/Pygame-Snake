from abc import ABC, abstractmethod

from src.actor.Actor import Actor


class Command(ABC):
    @abstractmethod
    def execute(self, actor: Actor):
        pass
