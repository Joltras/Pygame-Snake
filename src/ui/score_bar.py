import pygame
from pygame import font, Rect

from src.utils.color import Color
from src.utils.globals import SQUARE_SIZE

SCORE_BAR_HEIGHT: int = 2 * SQUARE_SIZE
BACKGROUND_COLOR: Color = Color.DARK_GRAY
TEXT_COLOR: Color = Color.WHITE
FONT_SIZE: int = 30
PADDING: int = 20


class ScoreBar:
    """
    Bar above the game field that shows the score.
    """

    def __init__(self, width: int, height: int = SCORE_BAR_HEIGHT):
        """
        Creates a new ScoreBar.
        :param width: width of the bar
        :param height: height of the bar
        """
        font.init()
        self._rect: Rect = Rect(0, 0, width, height)
        self._font = font.SysFont("Arial", FONT_SIZE)

    def get_height(self) -> int:
        """
        Returns the height of the bar.
        :return: height
        """
        return self._rect.height

    def draw(self, screen, score: int) -> None:
        """
        Draws the bar with the given score on the screen.
        :param screen: Screen to draw the bar on
        :param score: Score to show
        """
        pygame.draw.rect(screen, BACKGROUND_COLOR.value, self._rect)
        text = self._font.render(f"Score: {score}", True, TEXT_COLOR.value)
        screen.blit(text, (self._rect.left + PADDING, self._rect.centery - text.get_height() // 2))
