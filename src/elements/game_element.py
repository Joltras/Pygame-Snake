from abc import ABC, abstractmethod


class GameElement(ABC):

    @abstractmethod
    def collides(self, rects) -> bool:
        pass

    @abstractmethod
    def draw(self, screen) -> None:
        pass
