from typing import Union

import pygame
from pygame import Rect
from pygame.surface import Surface, SurfaceType

from food import Food
from game_field import GameField
from src.ui import message
from src.ui.buttons.button.image_button import ImageButton
from src.ui.buttons.button.text_button import TextButton
from src.utils.color import Color
from src.utils.game_state import GameState
from src.utils.globals import SQUARE_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT, FIELD_COLOR
from src.actor.snake_actor import Snake
from src.commands.command import Command
from src.commands.grow import GrowCommand
from src.commands.move_commands import MoveUpCommand, MoveDownCommand, MoveLeftCommand, MoveRightCommand
from src.ui.message import MessageDisplayer

START_BUTTON_IMAGE = pygame.image.load("StartButton.png")


class Game:
    _screen: Union[Surface, SurfaceType]
    _actor: Snake
    _field: GameField
    grow: GrowCommand

    def __init__(self, width: int, height: int):
        """
        Creates a new Game with the given data.
        :param width: width of the game window
        :param height: height of the game window
        """

        placed_food: bool

        self._field: GameField = GameField(width=width, height= height)

        self._actor: Snake = Snake(self._field.random_x_on_field(), self._field.random_y_on_field(),
                                   self._field.get_top(), self._field.get_left())
        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()

        self._message_displayer: MessageDisplayer = MessageDisplayer(self._field.get_width(),
                                                                     self._field.get_height(), self._field.get_top(),
                                                                     self._field.get_left())
        self.__food: Food
        self._set_food()

        self._game_state: GameState = GameState.STARTING
        self._start_button = ImageButton(START_BUTTON_IMAGE, self.set_running)
        self._exit_button = TextButton(Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), "Exit", self.set_closing, Color.ORANGE)
        self._restart_button = TextButton(Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), "Restart", self.set_starting)
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

    def _set_food(self) -> None:
        """
        Placed a new food object on the field
        """
        placed_food = False
        while not placed_food:
            x = self._field.random_x_on_field()
            y = self._field.random_y_on_field()
            self.__food = Food(x, y, self._field.get_top(), self._field.get_left())
            if not self._actor.collides_with_body(self.__food.get_rect()):
                placed_food = True

    def draw(self):
        """
        Draws all the objects.
        """
        self._screen.fill(Color.WHITE.value)
        pygame.draw.rect(self._screen, FIELD_COLOR.value, self._field.get_rect())
        self._field.draw(self._screen)

        for rect in self._actor.get_segments():
            pygame.draw.rect(self._screen, Color.GREEN.value, rect)
            pygame.draw.rect(self._screen, Color.DARK_GREEN.value, rect, 2, 1)

        pygame.draw.rect(self._screen, Color.BLACK.value, self.__food.get_rect())
        pygame.draw.rect(self._screen, Color.DARK_GRAY.value, self.__food.get_rect(), 2, 1)

    def run(self):
        """
        Reacts to the input.
        """
        active: bool
        command: Command = None

        active = True
        while active:

            if self._game_state.value == 0:
                # Starting
                self._starting()

            elif self._game_state.value == 1:
                # Running
                command = self._running(command)

            elif self._game_state.value == 2:
                # Winning
                print("WON!")

            elif self._game_state.value == 3:
                # Losing
                self._losing()

            elif self._game_state.value == 4:
                # Closing
                active = False
            elif self._game_state.value == 5:
                # Pausing
                self._pausing()

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

    def _running(self, command: Command) -> Command:
        """
        Reacts to the inputs while in game state running.
        :param command: current command
        :return: new command if changed otherwise the given command
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_state = GameState.CLOSE_GAME
                return command
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._game_state = GameState.PAUSED
                    return command
                n_command = self.handle_input(event)
                if n_command is not None:
                    command = n_command
        if command is not None:
            command.execute(self._actor)
            if self._field.collides_with_boarder(self._actor.get_segments()):
                self._game_state = GameState.GAME_OVER
            elif self._actor.collides_with_itself():
                self._game_state = GameState.GAME_OVER
            elif self._actor.collides_with_head(self.__food.get_rect()):
                self._set_food()
                self.grow.execute(self._actor)
        self.draw()
        return command

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

    def _losing(self) -> None:
        """
         Displays the losing message and reacts to input.
        """
        self._message_displayer.create_message(self._field, message.GAME_OVER_TITLE, self._screen,
                                               self._restart_button,
                                               self._exit_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_state = GameState.CLOSE_GAME
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self._actor = Snake(self._field.random_x_on_field(), self._field.random_y_on_field(),
                                        self._field.get_top(), self._field.get_left())
                    self._game_state = GameState.STARTING
                elif event.key == pygame.K_n:
                    self._game_state = GameState.CLOSE_GAME
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._exit_button.has_been_clicked(event.pos[0], event.pos[1])
                self._restart_button.has_been_clicked(event.pos[0], event.pos[1])
                if self._game_state.value == 0:
                    self._actor = Snake(self._field.random_x_on_field(), self._field.random_y_on_field(),
                                        self._field.get_top(), self._field.get_left())

    def handle_input(self, event) -> Command:
        """
        Checks the event and returns the corresponding command.
        :param event: event
        :return: command
        """
        command: Command = None
        if event.key == pygame.K_DOWN:
            command = self.move_down
        elif event.key == pygame.K_UP:
            command = self.move_up
        elif event.key == pygame.K_RIGHT:
            command = self.move_right
        elif event.key == pygame.K_LEFT:
            command = self.move_left

        return command
