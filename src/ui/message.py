import pygame
from pygame import font, Rect

from src.ui.buttons.button.button import Button
from src.utils.globals import Color
from src.elements.game_field import GameField

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

BUTTON_GAP: int = 40
BUTTON_MARGIN: int = 60


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

    def create_message(self, field: GameField, text: str, screen, button1: Button, button2: Button):
        """
        Creates a message and displays it within the given field on the given screen.
        :param field: GameField
        :param text: Message text
        :param screen: Screen
        :param button1: Left button
        :param button2: Right button
        """
        pygame.draw.rect(screen, BACKGROUND_COLOR, self.__background)
        center_x: int = field.get_width() // 2 + self.__left
        center_y: int = field.get_height() // 2 + self.__top + BUTTON_MARGIN

        self.create_title_message(field, text, screen)

        # Center both buttons as one row with a gap between them
        row_width: int = button1.get_width() + BUTTON_GAP + button2.get_width()
        x_pos: int = center_x - row_width // 2
        button1.draw(screen, x_pos, center_y - button1.get_height() // 2)
        button2.draw(screen, x_pos + button1.get_width() + BUTTON_GAP, center_y - button2.get_height() // 2)

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
