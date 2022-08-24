from pygame import Rect


class GameField:

    def __init__(self, width_in_squares, height_in_squares, square_size):
        """
        Creates a new GameField with the given data.
        :param width_in_squares: numbers of squares that fit a row of the field
        :param height_in_squares: number of squares that fit in a column of the field
        :param square_size: size of one square
        """
        self.__width_in_squares = width_in_squares
        self.__width = width_in_squares * square_size

        self.__height_in_squares = height_in_squares
        self.__height = height_in_squares * square_size

        self.__square_size = square_size

        # Create the border of the field
        self.__border = []
        i = 0
        while i < height_in_squares:
            if i == 0 or i == height_in_squares - 1:
                j = 0
                while j < width_in_squares:
                    self.__border.append(Rect(j * square_size, i * square_size, square_size, square_size))
                    j += 1
            else:
                self.__border.append(Rect(0, i * square_size, square_size, square_size))
                self.__border.append(
                    Rect((width_in_squares * square_size) - square_size, i * square_size, square_size, square_size))
            i += 1

    def get_width(self) -> int:
        """
        Returns the width of the field.
        :return: width
        """
        return self.__width

    def get_width_in_squares(self) -> int:
        """
        Returns how many squares can fit in a row of the field.
        :return: number of squares
        """
        return self.__width_in_squares

    def get_height(self) -> int:
        """
        Returns the height of the field.
        :return: height
        """
        return self.__height

    def get_height_in_squares(self):
        """
        Returns how many squares can fit in a column of the field.
        :return: number of squares
        """
        return self.__height_in_squares

    def get_square_size(self):
        """
        Returns the size of one square.
        :return: Size of a square
        """
        return self.__square_size

    def get_border(self) -> list:
        """
        Returns the border of the field as a list of rectangles.
        :return: Border of the field
        """
        return self.__border
