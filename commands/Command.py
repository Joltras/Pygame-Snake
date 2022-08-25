from abc import ABC, abstractmethod

from actor.Actor import Actor


class Command(ABC):
    @abstractmethod
    def execute(self, actor: Actor):
        pass
