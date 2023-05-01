from abc import ABC, abstractmethod
from typing import List


class GameElement(ABC):

    @abstractmethod
    def collides(self, rects) -> bool:
        pass

    @abstractmethod
    def draw(self, screen) -> None:
        pass
