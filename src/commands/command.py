from abc import ABC, abstractmethod

from src.actor.actor import Actor


class Command(ABC):
    @abstractmethod
    def execute(self, actor: Actor):
        pass
