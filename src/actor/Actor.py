from abc import abstractmethod, ABC


class Actor(ABC):
    @abstractmethod
    def move_up(self) -> None:
        """
        Moves the actor up.
        """
        pass

    @abstractmethod
    def move_down(self) -> None:
        """
        Moves the actor down.
        """
        pass

    @abstractmethod
    def move_left(self) -> None:
        """
        Moves the actor left.
        """
        pass

    @abstractmethod
    def move_right(self) -> None:
        """
        Moves the actor right.
        """
        pass

    @abstractmethod
    def grow(self) -> None:
        """
        Actor grows.
        """
        pass
