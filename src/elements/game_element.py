from abc import ABC, abstractmethod
from typing import List


class GameElement(ABC):

    @abstractmethod
    def draw(self, screen):
        pass
