from src.ui.buttons.button.button import Button


class ImageButton(Button):

    def __init__(self, image, on_click):
        super().__init__(image.get_rect(), on_click)
        self._image = image

    def draw(self, screen, x: int, y: int) -> None:
        self._rect.top = y
        self._rect.left = x
        screen.blit(self._image, (x, y))
