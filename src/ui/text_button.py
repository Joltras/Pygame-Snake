from abc import ABC, abstractmethod

import pygame.draw
from pygame import Rect, font
from src.utils.globals import Color

TEXT_COLOR: Color = Color.BLACK
FONT_SIZE = 25


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


class TextButton(Button):

    def __init__(self, rect, text, on_click, color=Color.GREEN):
        """
        Creates a new button with the given data.
        :param text: Text of the button
        :param on_click: On click function
        :param color: Color of the button
        """
        super().__init__(rect, on_click)
        self._text = text
        self._font = font.SysFont("Arial", FONT_SIZE)
        self._color = color

    def draw(self, screen, x: int, y: int) -> None:
        """
        Draws the button on the screen.
        :param screen: The screen to draw the button on
        :param x: x-coordinate of the button
        :param y: y-coordinate of the button
        """
        self._rect.top = y
        self._rect.left = x
        pygame.draw.rect(screen, self._color.value, self._rect)
        # calculate the center of the button
        text_x = x + self._rect.width / 2 - self._font.size(self._text)[0] / 2
        text_y = y + self._rect.height / 2 - self._font.size(self._text)[1] / 2

        rendered_font = self._font.render(self._text, True, TEXT_COLOR.value)
        screen.blit(rendered_font, (text_x, text_y))


class ImageButton(Button):

    def __init__(self, image, on_click):
        super().__init__(image.get_rect(), on_click)
        self._image = image

    def draw(self, screen, x: int, y: int) -> None:
        self._rect.top = y
        self._rect.left = x
        screen.blit(self._image, (x, y))
