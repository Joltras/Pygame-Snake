import pygame.draw
from pygame import Rect, font
from src.Globals import Color

TEXT_COLOR: Color = Color.BLACK
FONT_SIZE = 25


class Button:

    def __init__(self, width, height, text, on_click, color=Color.GREEN):
        """
        Creates a new button with the given data.
        :param width: Width of the button
        :param height: Height of the button
        :param text: Text of the button
        :param on_click: On click function
        :param color: Color of the button
        """
        self.__rect = None
        self.__text = text
        self.__font = font.SysFont("Arial", FONT_SIZE)
        self.__on_click = on_click
        self.__width = width
        self.__height = height
        self.__color = color

    def draw(self, screen, x: int, y: int) -> None:
        """
        Draws the button on the screen.
        :param screen: The screen to draw the button on
        :param x: x-coordinate of the button
        :param y: y-coordinate of the button
        """
        self.__rect = Rect(x, y, self.__width, self.__height)
        pygame.draw.rect(screen, self.__color.value, self.__rect)
        # calculate the center of the button
        text_x = x + self.__width / 2 - self.__font.size(self.__text)[0] / 2
        text_y = y + self.__height / 2 - self.__font.size(self.__text)[1] / 2

        rendered_font = self.__font.render(self.__text, True, TEXT_COLOR.value)
        screen.blit(rendered_font, (text_x, text_y))

    def has_been_clicked(self, x: int, y: int) -> None:
        """
        Checks if the button has been clicked.
        :param x: x-coordinate of the click
        :param y: y-coordinate of the click
        :return: True if the button has been clicked, False otherwise
        """
        if self.__rect.collidepoint(x, y):
            self.__on_click()

    def get_width(self) -> int:
        """
        Returns the width of the button.
        :return: The width of the button
        """
        return self.__width

    def get_height(self) -> int:
        """
        Returns the height of the button.
        :return: Height of the button
        """
        return self.__height
