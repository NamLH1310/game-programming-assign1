from dataclasses import dataclass

import pygame
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game_over = False

    # game loop
    while not game_over:
        # single keystroke
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True

        clock.tick(FPS)
        # redraw

    pygame.quit()


if __name__ == '__main__':
    main()
