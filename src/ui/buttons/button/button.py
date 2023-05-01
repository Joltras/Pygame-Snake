from abc import abstractmethod, ABC

from pygame import Rect


class Button(ABC):
    def __init__(self, rect, on_click):
        self._rect: Rect = rect
        self._on_click = on_click

    @abstractmethod
    def draw(self, screen, x: int, y: int):
        pass

    def has_been_clicked(self, x: int, y: int) -> None:
        """
        Checks if the button has been clicked.
        :param x: x-coordinate of the click
        :param y: y-coordinate of the click
        """
        if self._rect.collidepoint(x, y):
            self._on_click()

    def get_width(self) -> int:
        """
        Returns the width of the button.
        :return: The width of the button
        """
        return self._rect.width

    def get_height(self) -> int:
        """
        Returns the height of the button.
        :return: Height of the button
        """
        return self._rect.height
