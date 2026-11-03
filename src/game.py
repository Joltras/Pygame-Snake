import random
from pathlib import Path

import pygame
from pygame import Rect

from src.commands.grow import GrowCommand
from src.commands.move_commands import MoveCommand, MoveUpCommand, MoveDownCommand, MoveLeftCommand, MoveRightCommand
from src.elements.actor.snake_actor import Snake
from src.elements.food import Food
from src.elements.game_field import GameField
from src.ui import message
from src.ui.buttons.button.image_button import ImageButton
from src.ui.buttons.button.text_button import TextButton
from src.ui.message import MessageDisplayer
from src.ui.score_bar import ScoreBar
from src.utils.color import Color
from src.utils.game_state import GameState
from src.utils.globals import BUTTON_WIDTH, BUTTON_HEIGHT

START_BUTTON_IMAGE = pygame.image.load(Path(__file__).parent / "StartButton.png")


class Game:

    def __init__(self, width: int, height: int):
        """
        Creates a new Game with the given data.
        :param width: width of the game window
        :param height: height of the game window
        """

        placed_food: bool

        self._score_bar: ScoreBar = ScoreBar(width)
        self._field: GameField = GameField(width=width, height=height - self._score_bar.get_height(),
                                           top=self._score_bar.get_height())

        self._actor: Snake
        self._food: Food
        self._command: MoveCommand
        self._score: int
        self._reset()

        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()

        self._message_displayer: MessageDisplayer = MessageDisplayer(self._field.get_width(),
                                                                     self._field.get_height(), self._field.get_top(),
                                                                     self._field.get_left())

        self._game_state: GameState = GameState.STARTING
        self._start_button = ImageButton(START_BUTTON_IMAGE, self.set_running)
        self._exit_button = TextButton(Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), "Exit", self.set_closing, Color.ORANGE)
        self._restart_button = TextButton(Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), "Restart", self.restart)
        self._continue_button = TextButton(Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), "Continue", self.set_running)

        self.move_up = MoveUpCommand()
        self.move_down = MoveDownCommand()
        self.move_left = MoveLeftCommand()
        self.move_right = MoveRightCommand()
        self.grow = GrowCommand()

    def set_running(self) -> None:
        """
         Sets the current game state to running.
        """
        self._game_state = GameState.RUNNING

    def set_closing(self) -> None:
        """
         Sets the current game state to closing.
        """
        self._game_state = GameState.CLOSE_GAME

    def set_starting(self) -> None:
        """
         Sets the current game state to starting.
        """
        self._game_state = GameState.STARTING

    def restart(self) -> None:
        """
        Resets the game and shows the starting message.
        """
        self._reset()
        self.set_starting()

    def _reset(self) -> None:
        """
        Places a new snake and new food on the field, removes the current direction and resets the score.
        """
        self._actor = Snake(self._field.random_x_on_field(), self._field.random_y_on_field(),
                            self._field.get_top(), self._field.get_left())
        self._set_food()
        self._command = None
        self._score = 0

    def _set_food(self) -> bool:
        """
        Places a new food object on a random square that is not covered by the snake.
        :return: True if the food has been placed, False if there is no free square left
        """
        free_squares = []
        for x, y in self._field.get_inner_squares():
            food = Food(x, y, self._field.get_top(), self._field.get_left())
            if not self._actor.collides([food.get_rect()]):
                free_squares.append(food)
        if not free_squares:
            return False
        self._food = random.choice(free_squares)
        return True

    def draw(self):
        """
        Draws all the objects.
        """
        self._screen.fill(Color.WHITE.value)
        self._field.draw(self._screen)
        self._actor.draw(self._screen)
        self._food.draw(self._screen)
        pygame.draw.rect(self._screen, Color.DARK_GRAY.value, self._food.get_rect(), 2, 1)

    def run(self):
        """
        Reacts to the input.
        """
        active: bool

        active = True
        while active:

            if self._game_state.value == 0:
                # Starting
                self._starting()

            elif self._game_state.value == 1:
                # Running
                self._running()

            elif self._game_state.value == 2:
                # Winning
                self._winning()

            elif self._game_state.value == 3:
                # Losing
                self._losing()

            elif self._game_state.value == 4:
                # Closing
                active = False
            elif self._game_state.value == 5:
                # Pausing
                self._pausing()

            self._score_bar.draw(self._screen, self._score)
            pygame.display.flip()
            self._clock.tick(5)

    def _starting(self) -> None:
        """
        Displays the starting message and reacts to input.
        """
        self._message_displayer.create_message(self._field, message.START_TITLE, self._screen,
                                               self._start_button, self._exit_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_state = GameState.CLOSE_GAME
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._game_state = GameState.RUNNING
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._start_button.has_been_clicked(event.pos[0], event.pos[1])
                self._exit_button.has_been_clicked(event.pos[0], event.pos[1])

    def _running(self) -> None:
        """
        Reacts to the inputs while in game state running.
        """
        # Command that has been executed last, the snake must not turn back into it
        last_command: MoveCommand = self._command
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_state = GameState.CLOSE_GAME
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._game_state = GameState.PAUSED
                    return
                n_command = self.handle_input(event)
                if n_command is not None and not n_command.is_opposite(last_command):
                    self._command = n_command
        if self._command is not None:
            self._command.execute(self._actor)
            if self._field.collides(self._actor.get_segments()):
                self._game_state = GameState.GAME_OVER
            elif self._actor.collides_with_itself():
                self._game_state = GameState.GAME_OVER
            elif self._actor.collides([self._food.get_rect()]):
                self.grow.execute(self._actor)
                self._score += 1
                if not self._set_food():
                    # The snake covers the whole field
                    self._game_state = GameState.WON
        self.draw()

    def _pausing(self) -> None:
        """
        Displays the pausing message and reacts to input.
        """
        self._message_displayer.create_message(self._field, message.PAUSED_TITLE, self._screen,
                                               self._continue_button, self._exit_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_state = GameState.CLOSE_GAME
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._game_state = GameState.RUNNING
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._exit_button.has_been_clicked(event.pos[0], event.pos[1])
                self._continue_button.has_been_clicked(event.pos[0], event.pos[1])

    def _winning(self) -> None:
        """
         Displays the winning message and reacts to input.
        """
        self._end_game(message.WIN_TITLE)

    def _losing(self) -> None:
        """
         Displays the losing message and reacts to input.
        """
        self._end_game(message.GAME_OVER_TITLE)

    def _end_game(self, title: str) -> None:
        """
        Displays the given title with the restart and exit button and reacts to input.
        :param title: Title of the message
        """
        self._message_displayer.create_message(self._field, title, self._screen,
                                               self._restart_button,
                                               self._exit_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_state = GameState.CLOSE_GAME
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self.restart()
                elif event.key == pygame.K_n:
                    self._game_state = GameState.CLOSE_GAME
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._exit_button.has_been_clicked(event.pos[0], event.pos[1])
                self._restart_button.has_been_clicked(event.pos[0], event.pos[1])

    def handle_input(self, event) -> MoveCommand:
        """
        Checks the event and returns the corresponding command.
        :param event: event
        :return: command
        """
        command: MoveCommand = None
        if event.key == pygame.K_DOWN:
            command = self.move_down
        elif event.key == pygame.K_UP:
            command = self.move_up
        elif event.key == pygame.K_RIGHT:
            command = self.move_right
        elif event.key == pygame.K_LEFT:
            command = self.move_left

        return command
