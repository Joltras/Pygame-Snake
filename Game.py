import pygame

from Food import Food
from actor.Snake_Actor import Snake
import Message
from Globals import Color, GameState, SQUARE_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT
from Message import MessageDisplayer
from Game_Field import GameField
from Button import Button
from commands.Command import Command
from commands.Grow import GrowCommand
from commands.Move_Commands import MoveUpCommand, MoveDownCommand, MoveLeftCommand, MoveRightCommand


class Game:
    grow: GrowCommand

    def __init__(self, width: int, height: int):
        """
        Creates a new Game with the given data.
        :param width: width of the game window
        :param height: height of the game window
        """

        placed_food: bool
        width_in_squares: int = width // SQUARE_SIZE
        height_in_squares: int = height // SQUARE_SIZE

        self.__field: GameField = GameField(width_in_squares, height_in_squares)

        self.__actor: Snake = Snake(self.__field.random_x_on_field(), self.__field.random_y_on_field())
        self.__screen = pygame.display.set_mode((width, height))
        self.__clock = pygame.time.Clock()

        self.__message_displayer: MessageDisplayer = MessageDisplayer(self.__field.get_width(),
                                                                      self.__field.get_height())
        self.__food: Food = None
        self.set_food()

        self.__game_state: GameState = GameState.STARTING
        self.__start_Button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Start", self.set_running)
        self.__exit_Button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Exit", self.set_closing, Color.ORANGE)
        self.__restart_Button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Restart", self.set_starting)
        self.__continue_Button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Continue", self.set_running)

        self.move_up = MoveUpCommand()
        self.move_down = MoveDownCommand()
        self.move_left = MoveLeftCommand()
        self.move_right = MoveRightCommand()
        self.grow = GrowCommand()

    def set_running(self):
        self.__game_state = GameState.RUNNING

    def set_closing(self):
        self.__game_state = GameState.CLOSE_GAME

    def set_starting(self):
        self.__game_state = GameState.STARTING

    def set_food(self):
        placed_food = False
        while not placed_food:
            x = self.__field.random_x_on_field()
            y = self.__field.random_y_on_field()
            self.__food = Food(x, y)
            if not self.__actor.collides_with_body(self.__food.get_rect()):
                placed_food = True

    def draw(self):
        """
        Draws all the objects.
        """
        self.__screen.fill(Color.WHITE.value)

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
                self.__message_displayer.create_message(self.__field, Message.START_TITLE, self.__screen,
                                                        self.__start_Button,
                                                        self.__exit_Button)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__game_state = GameState.CLOSE_GAME
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.__game_state = GameState.RUNNING
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.__start_Button.has_been_clicked(event.pos[0], event.pos[1])
                        self.__exit_Button.has_been_clicked(event.pos[0], event.pos[1])

            elif self.__game_state.value == 1:
                # Running

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        active = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.__game_state = GameState.PAUSED
                            break
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
                        self.set_food()
                        self.grow.execute(self.__actor)
                self.draw()

            elif self.__game_state.value == 2:
                # Winning
                print("WON!")

            elif self.__game_state.value == 3:
                # Losing
                self.__message_displayer.create_message(self.__field, Message.GAME_OVER_TITLE, self.__screen,
                                                        self.__restart_Button,
                                                        self.__exit_Button)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__game_state = GameState.CLOSE_GAME
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            self.__actor = Snake(self.__field.random_x_on_field(), self.__field.random_y_on_field())
                            self.__game_state = GameState.STARTING
                        elif event.key == pygame.K_n:
                            self.__game_state = GameState.CLOSE_GAME
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.__exit_Button.has_been_clicked(event.pos[0], event.pos[1])
                        self.__restart_Button.has_been_clicked(event.pos[0], event.pos[1])
                        if self.__game_state.value == 0:
                            self.__actor = Snake(self.__field.random_x_on_field(), self.__field.random_y_on_field())

            elif self.__game_state.value == 4:
                # Closing
                active = False
            elif self.__game_state.value == 5:
                # Pausing
                self.__message_displayer.create_message(self.__field, Message.PAUSED_TITLE, self.__screen,
                                                        self.__continue_Button, self.__exit_Button)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__game_state = GameState.CLOSE_GAME
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.__game_state = GameState.RUNNING
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.__exit_Button.has_been_clicked(event.pos[0], event.pos[1])
                        self.__continue_Button.has_been_clicked(event.pos[0], event.pos[1])

            pygame.display.flip()
            self.__clock.tick(5)

    def handle_input(self, event) -> Command:
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
