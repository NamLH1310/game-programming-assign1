from pygame.locals import *
from SpriteSheet import *
import time

##############################################
# Screen settings

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
##############################################
# Timer settings
TIMER = 60


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


def render_end_screen():
    
    game_over_txt = pygame.font.Font(None, 40).render("GAME OVER", True, pygame.Color('white'))
    retry_txt = pygame.font.Font(None,35).render("Press R to Retry", True, pygame.Color('white'))
    quit_txt = pygame.font.Font(None, 35).render("Press Q to Quit", True, pygame.Color('white'))

    screen.blit(game_over_txt, ((SCREEN_WIDTH - game_over_txt.get_width()) / 2, (SCREEN_HEIGHT - game_over_txt.get_height()) /2 - SCREEN_HEIGHT / 15))
    screen.blit(retry_txt, ((SCREEN_WIDTH - retry_txt.get_width()) / 2, (SCREEN_HEIGHT - retry_txt.get_height()) / 2))
    screen.blit(quit_txt, ((SCREEN_WIDTH - quit_txt.get_width()) / 2, (SCREEN_HEIGHT - quit_txt.get_height()) / 2 + SCREEN_HEIGHT / 15))
    pygame.display.flip()
    pass

# Main func
def main() -> None:
    count = 0  # for debug only

    clock = pygame.time.Clock()
    game_over = False

    # (Delta time since last tick)
    timer = TIMER
    dt = 0

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

        
        
        # Prompt end-game screen
        timer -= dt
        if timer <= 0:
            timer = 0
            get_event = False
            render_end_screen()
            while not get_event:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = get_event = True
                            break
                        elif event.key == pygame.K_r:
                            get_event = True
                            timer = TIMER
                            clock = pygame.time.Clock()
                            break


        # Displaying remaining time
        txt = pygame.font.Font(None, 40).render(str(round(timer, 2)), True, pygame.Color('black'))
        screen.blit(txt, (5, 5))
        pygame.display.flip()
        dt = clock.tick(30) / 500  



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
