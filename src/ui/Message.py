import pygame
from pygame import font, Rect

from src.Globals import Color
from src.Game_Field import GameField
from src.ui.TextButton import TextButton

START_TITLE: str = "SNAKE"
START_MESSAGE: str = "Press the button to start"

BACKGROUND_COLOR: tuple = Color.LIGHT_GRAY.value

TITLE_COLOR: tuple = Color.DARK_GREEN.value
TITLE_FONT_SIZE: int = 60

MESSAGE_COLOR: tuple = Color.BLACK.value
MESSAGE_FONT_SIZE: int = int(TITLE_FONT_SIZE * 0.75)

GAME_OVER_TITLE: str = "Game Over!"

WIN_TITLE: str = "WON"

PAUSED_TITLE: str = "Paused"


class MessageDisplayer:
    """
    Object of this class create Messages with given Colors and Fonts.
    """

    def __init__(self, width, height, top: int, left: int):
        """
        Creates a new MessageDisplayer.
        :param width: Width of the message
        :param height: Height of the message
        :param top: y offset
        :param left: x offset
        """
        font.init()
        self.__top = top
        self.__left = left
        self.__background: Rect = Rect(left, top, width, height)
        self.__title_font = font.SysFont(font.get_default_font(), TITLE_FONT_SIZE)

    def create_message(self, field: GameField, text: str, screen, button1: TextButton, button2: TextButton):
        """
        Creates a message and displays it within the given field on the given screen.
        :param field: GameField
        :param text: Message text
        :param screen: Screen
        """
        pygame.draw.rect(screen, BACKGROUND_COLOR, self.__background)
        y_pos: int = field.get_height() // 2
        x_pos: int = field.get_height() // 2

        self.create_title_message(field, text, screen)
        button1.draw(screen, x_pos - button1.get_width() + self.__left, y_pos + button1.get_height() + self.__top)
        button2.draw(screen, x_pos + button2.get_width() + self.__left, y_pos + button2.get_height() + self.__top)

    def create_title_message(self, field: GameField, text: str, screen):
        """
        Creates a Title and displays it on the screen.
        :param field: GameField
        :param text: Title text
        :param screen: Screen to place the title on
        """
        title = self.__title_font.render(text, True, TITLE_COLOR)
        y_pos = field.get_height() / 2 - self.__title_font.size(text)[1] / 2 + self.__top
        x_pos = field.get_width() / 2 - self.__title_font.size(text)[0] / 2 + self.__left

        screen.blit(title, (x_pos, y_pos - title.get_height()))


