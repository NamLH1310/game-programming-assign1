import random

from pygame.locals import *

from SpriteSheet import *
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TIMER, MAX_ZOMBIES

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


# sprite_list = zombie.get_sprites()

class EntitySystem:
    def __init__(self):
        self.entities = set[Zombie]()
        self.deleted_entities = list[Zombie]()

    def generate_random_zombie(self):
        if len(self.entities) <= MAX_ZOMBIES and random.randint(0, 1) == 1:
            self.entities.add(Zombie(screen=canvas,
                                     filename='./image/zombie.png',
                                     w=35,
                                     h=70,
                                     x=random.randint(0, SCREEN_WIDTH - 35),
                                     y=random.randint((SCREEN_HEIGHT >> 1) - 140, SCREEN_HEIGHT >> 1),
                                     velocity=random.randint(20, 30)))

    def draw(self):
        self.generate_random_zombie()

        for z in self.entities:
            if z.is_dead:
                self.deleted_entities.append(z)
            else:
                z.draw()

        for z in self.deleted_entities:
            self.entities.remove(z)

        self.deleted_entities.clear()


def render_end_screen():
    game_over_txt = pygame.font.Font(None, 40).render("GAME OVER", True, pygame.Color('white'))
    retry_txt = pygame.font.Font(None, 35).render("Press R to Retry", True, pygame.Color('white'))
    quit_txt = pygame.font.Font(None, 35).render("Press Q to Quit", True, pygame.Color('white'))

    screen.blit(game_over_txt, ((SCREEN_WIDTH - game_over_txt.get_width()) // 2,
                                (SCREEN_HEIGHT - game_over_txt.get_height()) // 2 - SCREEN_HEIGHT // 15))
    screen.blit(retry_txt, ((SCREEN_WIDTH - retry_txt.get_width()) // 2, (SCREEN_HEIGHT - retry_txt.get_height()) // 2))
    screen.blit(quit_txt, (
        (SCREEN_WIDTH - quit_txt.get_width()) // 2, (SCREEN_HEIGHT - quit_txt.get_height()) // 2 + SCREEN_HEIGHT // 15))
    pygame.display.flip()


def draw(entities: EntitySystem) -> None:
    canvas.fill((255, 255, 255))
    canvas.blit(bg, (0, 0))

    # Zombie
    entities.draw()
    # Mouse
    canvas.blit(target, target_rect)
    canvas.blit(gun, gun_rect)

    # Reattach canvas
    screen.blit(canvas, (0, 0))
    pygame.display.update()


# Main func
def main() -> None:
    clock = pygame.time.Clock()
    game_over = False

    # (Delta time since last tick)
    timer = TIMER
    delta_t = 0
    entities = EntitySystem()
    entities.generate_random_zombie()
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

        # count = (count + 1) % len(sprite_list)

        # Prompt end-game screen
        timer -= delta_t
        if timer <= 0:
            timer = 0
            get_event = False
            render_end_screen()
            while not get_event:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        game_over = get_event = True

                    if event.type != pygame.KEYDOWN:
                        continue

                    match event.key:
                        case pygame.K_q:
                            game_over = get_event = True
                        case pygame.K_r:
                            get_event = True
                            timer = TIMER

        # Displaying remaining time
        txt = pygame.font.Font(None, 40).render(str(round(timer, 2)), True, pygame.Color('black'))
        screen.blit(txt, (5, 5))
        pygame.display.flip()
        delta_t = clock.tick(FPS) / 1000

        # redraw
        draw(entities)

    pygame.quit()


if __name__ == '__main__':
    main()
