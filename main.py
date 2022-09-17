from pygame.locals import *

from SpriteSheet import *

##############################################
# Screen settings

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

##############################################
pygame.init()

# Init screen
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mouse.set_visible(False)

# Background
bg = Aim('./image/empty_field.png').draw(SCREEN_WIDTH, SCREEN_HEIGHT)

# Cursor param
target = Aim('./image/aim.png').draw(SCREEN_WIDTH // 8, SCREEN_WIDTH // 8)
gun = Aim('./image/gun.png').draw(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)
target_rect = target.get_rect()
gun_rect = gun.get_rect()

# Import char sprite
zombie = Zombie('./image/zombie.png', SCREEN_WIDTH // 8, SCREEN_WIDTH // 7)
sprite_list = zombie.draw_demo()


# Main func
def main() -> None:
    count = 0  # for debug only

    clock = pygame.time.Clock()
    game_over = False

    # game loop
    while not game_over:

        # mouse movement
        x, y = pygame.mouse.get_pos()
        gun_rect.center = (x - SCREEN_WIDTH / 11, y + SCREEN_WIDTH / 11)

        target_rect.center = (x, y)

        # single keystroke
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:  # For debug only
                if event.key == pygame.K_SPACE:
                    count = int((count + 1) % len(sprite_list))

        clock.tick(FPS)

        # redraw
        canvas.fill((255, 255, 255))
        canvas.blit(bg, (0, 0))

        # Zombie
        canvas.blit(sprite_list[count], (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))

        # Mouse
        canvas.blit(target, target_rect)
        canvas.blit(gun, gun_rect)

        # Reattach canvas
        screen.blit(canvas, (0, 0))
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
