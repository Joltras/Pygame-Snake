from abc import abstractmethod, ABC


class Actor(ABC):
    @abstractmethod
    def move_up(self) -> None:
        pass

    @abstractmethod
    def move_down(self) -> None:
        pass

    @abstractmethod
    def move_left(self) -> None:
        pass

    @abstractmethod
    def move_right(self) -> None:
        pass

    @abstractmethod
    def grow(self) -> None:
        pass
