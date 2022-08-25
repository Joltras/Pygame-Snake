from pygame import Rect
from Enums import Direction
from Food import Food
from Game_Field import GameField
import random


class Snake:
    def __init__(self, field: GameField):
        """
        Creates a new Snake and places it on a random position on the field.
        :param field: Game field
        """
        self.__moving_direction = Direction.DOWN

        # Create and place the head of the snake
        self.__segments = []
        left = random.randint(1, (field.get_width_in_squares() - 2))
        top = random.randint(1, (field.get_height_in_squares() - 2))
        size = field.get_square_size()
        rect = Rect(left * size, top * size, size, size)
        self.__segments.append(rect)

        # Place the food
        self.__food = Food(field)
        self.place_food(field)

    def get_segments(self) -> list:
        """
        Returns the segments of the snake as a list of rectangles.
        :return: Segments of the snake
        """
        return self.__segments

    def get_length(self) -> int:
        """
        Returns the length of the snake.
        :return: Length
        """
        return len(self.__segments)

    def get_head(self) -> Rect:
        """
        Returns the head of the snake (first segment).
        :return: Head of the snake
        """
        return self.__segments[0]

    def get_food(self) -> Food:
        """
        Returns the food object
        :return: Food
        """
        return self.__food

    def change_direction(self, direction: Direction):
        """
        Changes the current moving direction of the snake.
        :param direction: New moving direction
        """
        self.__moving_direction = direction

    def get_direction(self) -> Direction:
        """
        Returns the current moving direction.
        :return: Moving direction
        """
        return self.__moving_direction

    def move(self, field: GameField) -> bool:
        """
        Moves the snake in the current direction within the field.
        Places the food anew if it hit the food.
        :param field: Field
        :return: False if it hit the borders of the field or itself, otherwise True
        """
        new_head: Rect = Rect(0, 0, 0, 0)
        old_head: Rect = self.get_head()
        segment: Rect

        collide: bool = False
        placed_food: bool

        i: int

        # Create a new head with current direction
        if self.__moving_direction is Direction.UP:
            new_head = old_head.move(0, -old_head.width)
        elif self.__moving_direction is Direction.DOWN:
            new_head = old_head.move(0, old_head.width)
        elif self.__moving_direction is Direction.LEFT:
            new_head = old_head.move(-old_head.width, 0)
        elif self.__moving_direction is Direction.RIGHT:
            new_head = old_head.move(old_head.width, 0)

        # Last segment
        segment = self.__segments[len(self.__segments) - 1]

        i = 0
        # Check for collision with itself
        collide = new_head.collidelist(self.__segments) != -1
        if collide:
            return False

        # Check for collision with the border of the field
        collide = new_head.top == 0 or new_head.top == (field.get_height() - field.get_square_size()) \
                  or new_head.left == 0 or new_head.left == (field.get_width() - field.get_square_size())
        if collide:
            return False

        # Check for collision with the food
        collide = new_head.colliderect(self.__food.get_rect())

        # Create a new body with new_head as head but without the last segment
        i = len(self.__segments) - 1
        while i > 0:
            self.__segments[i] = self.__segments[i - 1]
            i -= 1

        self.__segments[0] = new_head

        if collide:
            # Put the last element back (for growth)
            self.__segments.append(segment)
            # Place the food till it is not placed within the snake
            self.place_food(field)

        return True

    def collides_with_rectangle(self, rect: Rect) -> bool:
        """
        Checks if the segments of the snake collide with a given rectangle.
        :param rect: Rectangle to check collision
        :return: True when they collide otherwise False
        """
        if rect.collidelist(self.__segments) != -1:
            return False
        else:
            return True

    def place_food(self, field: GameField):
        """
        Places the Food on the field.
        Makes sure that the snake and the food doesn't collide
        :param field: Field to place the food on
        """
        placed_food: bool = False

        while not placed_food:
            self.__food.place(field)
            placed_food = self.collides_with_rectangle(self.__food.get_rect())
