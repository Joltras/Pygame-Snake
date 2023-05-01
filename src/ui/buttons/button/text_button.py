import pygame.draw
from pygame import font

from src.ui.buttons.button.button import Button
from src.utils.globals import Color

TEXT_COLOR: Color = Color.BLACK
FONT_SIZE = 25


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

