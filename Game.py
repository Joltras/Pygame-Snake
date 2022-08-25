import pygame
from actor.Snake import Snake
import Message
from Enums import Direction, Color, GameState
from Message import MessageDisplayer
from Game_Field import GameField
from Button import Button
from commands.Command import Command
from commands.Move_Commands import MoveUpCommand, MoveDownCommand, MoveLeftCommand, MoveRightCommand

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
NUMBER_OF_SQUARES = 50
SQUARE_SIZE = 20

class Game:
    def __init__(self, width: int, height: int):
        """
        Creates a new Game with the given data.
        :param width_in_squares: Numbers of squares that can fit in a row of the game field.
        :param height_in_squares: Numbers of squares that can fit in a column of the field
        :param square_size: Size of one field
        """
        placed_food: bool
        width_in_squares: int = width // SQUARE_SIZE
        height_in_squares: int = height // SQUARE_SIZE

        self.__field: GameField = GameField(width_in_squares, height_in_squares, SQUARE_SIZE)
        self.__snake: Snake = Snake(self.__field)
        self.__screen = pygame.display.set_mode((width, height))
        self.__clock = pygame.time.Clock()

        self.__message_displayer: MessageDisplayer = MessageDisplayer(self.__field.get_width(),
                                                                      self.__field.get_height())

        self.__game_state: GameState = GameState.STARTING
        self.__start_Button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Start", self.set_running)
        self.__exit_Button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Exit", self.set_closing, Color.ORANGE)
        self.__restart_Button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Restart", self.set_starting)
        self.__continue_Button = Button(BUTTON_WIDTH, BUTTON_HEIGHT, "Continue", self.set_running)

        self.move_up = MoveUpCommand()
        self.move_down = MoveDownCommand()
        self.move_left = MoveLeftCommand()
        self.move_right = MoveRightCommand()

    def set_running(self):
        self.__game_state = GameState.RUNNING

    def set_closing(self):
        self.__game_state = GameState.CLOSE_GAME

    def set_starting(self):
        self.__game_state = GameState.STARTING

    def draw(self):
        """
        Draws all the objects.
        """
        self.__screen.fill(Color.WHITE.value)

        for rect in self.__field.get_border():
            pygame.draw.rect(self.__screen, Color.LIGHT_GRAY.value, rect)
            pygame.draw.rect(self.__screen, Color.GRAY.value, rect, 2, 1)

        for rect in self.__snake.get_segments():
            pygame.draw.rect(self.__screen, Color.GREEN.value, rect)
            pygame.draw.rect(self.__screen, Color.DARK_GREEN.value, rect, 2, 1)

        pygame.draw.rect(self.__screen, Color.BLACK.value, self.__snake.get_food().get_rect())
        pygame.draw.rect(self.__screen, Color.DARK_GRAY.value, self.__snake.get_food().get_rect(), 2, 1)

    def run(self):
        """
        Reacts to the input.
        """
        active: bool
        first_input = True

        active = True
        while active:

            if self.__game_state.value == 0:
                # Starting
                self.__message_displayer.create_message(self.__field, Message.START_TITLE,  self.__screen,  self.__start_Button,
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
                        first_input = not self.check_movement(event)
                if not first_input:
                    if not self.__snake.move(self.__field):
                        self.__game_state = GameState.GAME_OVER
                self.draw()

            elif self.__game_state.value == 2:
                # Winning
                print("WON!")

            elif self.__game_state.value == 3:
                # Losing
                self.__message_displayer.create_message(self.__field,Message.GAME_OVER_TITLE, self.__screen, self.__restart_Button,
                                                           self.__exit_Button)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__game_state = GameState.CLOSE_GAME
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            self.__snake = Snake(self.__field)
                            first_input = True
                            self.__game_state = GameState.STARTING
                        elif event.key == pygame.K_n:
                            self.__game_state = GameState.CLOSE_GAME
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.__exit_Button.has_been_clicked(event.pos[0], event.pos[1])
                        self.__restart_Button.has_been_clicked(event.pos[0], event.pos[1])
                        if self.__game_state.value == 0:
                            self.__snake = Snake(self.__field)
                            first_input = True

            elif self.__game_state.value == 4:
                # Closing
                active = False
            elif self.__game_state.value == 5:
                # Pausing
                self.__message_displayer.create_message(self.__field, Message.PAUSED_TITLE, self.__screen, self.__continue_Button, self.__exit_Button)
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


    def check_movement(self, event) -> bool:
        """
        Change the direction when a arrow key was pressed.
        :param event: Event
        :return: True when the direction changed otherwise False
        """
        changed_direction: bool = False

        if event.key == pygame.K_DOWN:
            self.__snake.change_direction(Direction.DOWN)
            changed_direction = True
        elif event.key == pygame.K_UP:
            self.__snake.change_direction(Direction.UP)
            changed_direction = True
        elif event.key == pygame.K_RIGHT:
            self.__snake.change_direction(Direction.RIGHT)
            changed_direction = True
        elif event.key == pygame.K_LEFT:
            self.__snake.change_direction(Direction.LEFT)
            changed_direction = True

        return changed_direction

    def handle_input(self, event)-> Command:
        command: Command = None

        if event.key == pygame.K_DOWN:
            self.__snake.change_direction(Direction.DOWN)
            command = self.move_down
        elif event.key == pygame.K_UP:
            self.__snake.change_direction(Direction.UP)
            command = self.move_up
        elif event.key == pygame.K_RIGHT:
            self.__snake.change_direction(Direction.RIGHT)
            command = self.move_right
        elif event.key == pygame.K_LEFT:
            self.__snake.change_direction(Direction.LEFT)
            command = self.move_left

        return command


