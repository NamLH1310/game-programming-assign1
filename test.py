from turtle import screensize
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

black = (0, 0, 0)
white = 255, 255, 255
RED = 200, 0, 0
GREEN = 0, 200, 0
BRIGHT_RED = 255, 0, 0
BRIGHT_GREEN = 0, 255, 0

block_color = 53, 115, 255

car_width = 73

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A bit Racey")
clock = pygame.time.Clock()

# text_objects = pygame.draw.rect(screen, "RED", (150,450,100,50))


def game_intro():

    intro = True

    game_over_txt = pygame.font.Font(None, 40).render(
        "GAME OVER", True, pygame.Color("black")
    )
    retry_txt = pygame.font.Font(None, 35).render("Retry", True, pygame.Color("black"))
    quit_txt = pygame.font.Font(None, 35).render("Quit", True, pygame.Color("black"))

    while intro:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        pygame.draw.rect(
            screen,
            "beige",
            (
                SCREEN_WIDTH // 4,
                SCREEN_HEIGHT // 4,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
            ),
        )

        screen.blit(
            game_over_txt,
            (
                (SCREEN_WIDTH - game_over_txt.get_width()) / 2,
                (SCREEN_HEIGHT - game_over_txt.get_height()) / 2 - SCREEN_HEIGHT / 15,
            ),
        )

        # pygame.draw.rect(screen, GREEN,(150,450,100,50))
        # pygame.draw.rect(screen, RED,(550,450,100,50))

        # if 100+100 > mouse[0] > 100 and 330+50 > mouse[1] > 330:
        #     pass
        # else:
        pygame.draw.rect(
            screen,
            GREEN,
            (
                SCREEN_WIDTH // 4,
                SCREEN_HEIGHT * 0.75 - SCREEN_HEIGHT // 12,
                SCREEN_WIDTH // 10,
                SCREEN_HEIGHT // 12,
            ),
        )
        pygame.draw.rect(
            screen,
            RED,
            (
                SCREEN_WIDTH * 0.75 - SCREEN_WIDTH // 10,
                SCREEN_HEIGHT * 0.75 - SCREEN_HEIGHT // 12,
                SCREEN_WIDTH // 10,
                SCREEN_HEIGHT // 12,
            ),
        )

        if (
            SCREEN_WIDTH // 4 + SCREEN_WIDTH // 10 > mouse[0] > SCREEN_WIDTH // 4
            and SCREEN_HEIGHT * 0.75 - SCREEN_HEIGHT // 12 < mouse[1] < SCREEN_HEIGHT * 0.75
        ):
            pygame.draw.rect(
                screen,
                BRIGHT_GREEN,
                (
                    SCREEN_WIDTH // 4,
                    SCREEN_HEIGHT * 0.75 - SCREEN_HEIGHT // 12,
                    SCREEN_WIDTH // 10,
                    SCREEN_HEIGHT // 12,
                ),
            )
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                pass

        if (
            SCREEN_WIDTH * 0.75 > mouse[0] > SCREEN_WIDTH * 0.75 - SCREEN_WIDTH // 10
            and SCREEN_HEIGHT * 0.75 > mouse[1] > SCREEN_HEIGHT * 0.75 - SCREEN_HEIGHT // 12
        ):
            pygame.draw.rect(
                screen,
                BRIGHT_RED,
                (
                    SCREEN_WIDTH * 0.75 - SCREEN_WIDTH // 10,
                    SCREEN_HEIGHT * 0.75 - SCREEN_HEIGHT // 12,
                    SCREEN_WIDTH // 10,
                    SCREEN_HEIGHT // 12,
                ),
            )
            click = pygame.mouse.get_pressed()

            if click[0] == 1:
                intro = False

        screen.blit(
            retry_txt,
            (
                SCREEN_WIDTH // 4 + SCREEN_WIDTH // 20 - retry_txt.get_width() / 2,
                SCREEN_HEIGHT * 0.75 + SCREEN_HEIGHT // 24 - SCREEN_HEIGHT // 12 - retry_txt.get_height() / 2,
            ),
        )
        screen.blit(
            quit_txt,
            (
                SCREEN_WIDTH * 0.75 - SCREEN_WIDTH // 10 + SCREEN_WIDTH // 20 - quit_txt.get_width() / 2,
                SCREEN_HEIGHT * 0.75 - SCREEN_HEIGHT // 12 + SCREEN_HEIGHT // 24 - quit_txt.get_height() / 2,
            ),
        )
        pygame.display.update()
        clock.tick(15)


game_intro()
