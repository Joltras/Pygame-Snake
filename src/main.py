import pygame

from game import Game

if __name__ == "__main__":
    pygame.init()
    info = pygame.display.Info()
    game = Game(info.current_w, info.current_h)
    game.run()
