from abc import ABC, abstractmethod
from typing import List
from pygame import Rect


class GameElement(ABC):

    @abstractmethod
    def collides(self, rects: List[Rect]) -> bool:
        pass

    @abstractmethod
    def draw(self, screen) -> None:
        pass
