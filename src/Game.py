from typing import Union

import pygame
from pygame import Rect
from pygame.surface import Surface, SurfaceType

from Food import Food
from Game_Field import GameField
from Globals import Color, GameState, SQUARE_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT, FIELD_COLOR
from src.actor.Snake_Actor import Snake
from src.commands.Command import Command
from src.commands.Grow import GrowCommand
from src.commands.Move_Commands import MoveUpCommand, MoveDownCommand, MoveLeftCommand, MoveRightCommand
from src.ui import Message
from src.ui.Button import Button
from src.ui.Message import MessageDisplayer


class Game:
    __screen: Union[Surface, SurfaceType]
    __actor: Snake
    __field: GameField
    grow: GrowCommand

    def __init__(self, width: int, height: int):
        """
        Creates a new Game with the given data.
        :param width: width of the game window
        :param height: height of the game window
        """

        field_width: int = int(width * 0.5)
        field_height: int = int(height * 0.8)
        placed_food: bool
        width_in_squares: int = field_width // SQUARE_SIZE
        height_in_squares: int = field_height // SQUARE_SIZE
        self.__info = Rect(width_in_squares // 2 * SQUARE_SIZE, height_in_squares * SQUARE_SIZE, width_in_squares * SQUARE_SIZE,
                           height * 0.2)

        self.__field: GameField = GameField(width_in_squares, height_in_squares, width_in_squares // 2 * SQUARE_SIZE,
                                            0)

        self.__actor: Snake = Snake(self.__field.random_x_on_field(), self.__field.random_y_on_field(), self.__field.get_top(), self.__field.get_left())
        self.__screen = pygame.display.set_mode((width, height))
        self.__clock = pygame.time.Clock()

        self.__message_displayer: MessageDisplayer = MessageDisplayer(self.__field.get_width(),
                                                                      self.__field.get_height(), self.__field.get_top(),
                                                                      self.__field.get_left())
        self.__food: Food
        self._set_food()

        self.__game_state: GameState = GameState.STARTING
        self.__start_button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Start", self.set_running)
        self.__exit_button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Exit", self.set_closing, Color.ORANGE)
        self.__restart_button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Restart", self.set_starting)
        self.__continue_button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Continue", self.set_running)

        self.move_up = MoveUpCommand()
        self.move_down = MoveDownCommand()
        self.move_left = MoveLeftCommand()
        self.move_right = MoveRightCommand()
        self.grow = GrowCommand()

    def set_running(self) -> None:
        """
         Sets the current game state to running.
        """
        self.__game_state = GameState.RUNNING

    def set_closing(self) -> None:
        """
         Sets the current game state to closing.
        """
        self.__game_state = GameState.CLOSE_GAME

    def set_starting(self) -> None:
        """
         Sets the current game state to starting.
        """
        self.__game_state = GameState.STARTING

    def _set_food(self) -> None:
        """
        Placed a new food object on the field
        """
        placed_food = False
        while not placed_food:
            x = self.__field.random_x_on_field()
            y = self.__field.random_y_on_field()
            self.__food = Food(x, y, self.__field.get_top(), self.__field.get_left())
            if not self.__actor.collides_with_body(self.__food.get_rect()):
                placed_food = True

    def draw(self):
        """
        Draws all the objects.
        """
        self.__screen.fill(Color.WHITE.value)
        pygame.draw.rect(self.__screen,Color.ORANGE.value, self.__info)
        pygame.draw.rect(self.__screen, FIELD_COLOR.value, self.__field.get_rect())
        for rect in self.__field.get_border():
            pygame.draw.rect(self.__screen, Color.LIGHT_GRAY.value, rect)
            pygame.draw.rect(self.__screen, Color.GRAY.value, rect, 2, 1)

        for rect in self.__actor.get_segments():
            pygame.draw.rect(self.__screen, Color.GREEN.value, rect)
            pygame.draw.rect(self.__screen, Color.DARK_GREEN.value, rect, 2, 1)

        pygame.draw.rect(self.__screen, Color.BLACK.value, self.__food.get_rect())
        pygame.draw.rect(self.__screen, Color.DARK_GRAY.value, self.__food.get_rect(), 2, 1)

    def run(self):
        """
        Reacts to the input.
        """
        active: bool
        command: Command = None

        active = True
        while active:

            if self.__game_state.value == 0:
                # Starting
                self._starting()

            elif self.__game_state.value == 1:
                # Running
                command = self._running(command)

            elif self.__game_state.value == 2:
                # Winning
                print("WON!")

            elif self.__game_state.value == 3:
                # Losing
                self._losing()

            elif self.__game_state.value == 4:
                # Closing
                active = False
            elif self.__game_state.value == 5:
                # Pausing
                self._pausing()

            pygame.display.flip()
            self.__clock.tick(5)

    def _starting(self) -> None:
        """
        Displays the starting message and reacts to input.
        """
        self.__message_displayer.create_message(self.__field, Message.START_TITLE, self.__screen,
                                                self.__start_button,
                                                self.__exit_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_state = GameState.CLOSE_GAME
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__game_state = GameState.RUNNING
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__start_button.has_been_clicked(event.pos[0], event.pos[1])
                self.__exit_button.has_been_clicked(event.pos[0], event.pos[1])

    def _running(self, command: Command) -> Command:
        """
        Reacts to the inputs while in game state running.
        :param command: current command
        :return: new command if changed otherwise the given command
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_state = GameState.CLOSE_GAME
                return command
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__game_state = GameState.PAUSED
                    return command
                n_command = self.handle_input(event)
                if n_command is not None:
                    command = n_command
        if command is not None:
            command.execute(self.__actor)
            if self.__field.collides_with_boarder(self.__actor.get_segments()):
                self.__game_state = GameState.GAME_OVER
            elif self.__actor.collides_with_itself():
                self.__game_state = GameState.GAME_OVER
            elif self.__actor.collides_with_head(self.__food.get_rect()):
                self._set_food()
                self.grow.execute(self.__actor)
        self.draw()
        return command

    def _pausing(self) -> None:
        """
        Displays the pausing message and reacts to input.
        """
        self.__message_displayer.create_message(self.__field, Message.PAUSED_TITLE, self.__screen,
                                                self.__continue_button, self.__exit_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_state = GameState.CLOSE_GAME
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__game_state = GameState.RUNNING
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__exit_button.has_been_clicked(event.pos[0], event.pos[1])
                self.__continue_button.has_been_clicked(event.pos[0], event.pos[1])

    def _losing(self) -> None:
        """
         Displays the losing message and reacts to input.
        """
        self.__message_displayer.create_message(self.__field, Message.GAME_OVER_TITLE, self.__screen,
                                                self.__restart_button,
                                                self.__exit_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_state = GameState.CLOSE_GAME
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self.__actor = Snake(self.__field.random_x_on_field(), self.__field.random_y_on_field(), self.__field.get_top(), self.__field.get_left())
                    self.__game_state = GameState.STARTING
                elif event.key == pygame.K_n:
                    self.__game_state = GameState.CLOSE_GAME
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__exit_button.has_been_clicked(event.pos[0], event.pos[1])
                self.__restart_button.has_been_clicked(event.pos[0], event.pos[1])
                if self.__game_state.value == 0:
                    self.__actor = Snake(self.__field.random_x_on_field(), self.__field.random_y_on_field(), self.__field.get_top(), self.__field.get_left())

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
