import random

from pygame.locals import *

from SpriteSheet import *
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TIMER, MAX_ZOMBIES

pygame.init()
# pygame.mixer.init()

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
# Sound
bgm = pygame.mixer.Sound('./sound/background.ogg')
gun_shot = pygame.mixer.Sound('./sound/gun-shot.ogg')
screams = pygame.mixer.Sound('./sound/screams.ogg')


# sprite_list = zombie.get_sprites()

class EntitySystem:
    def __init__(self):
        self.entities = set[Zombie]()
        self.deleted_entities = list[Zombie]()
        self.Kill = 0

    def generate_random_zombie(self):
        if len(self.entities) <= MAX_ZOMBIES and random.randint(0, 1) == 1:
            self.entities.add(Zombie(screen=canvas,
                                     filename='./image/zombie.png',
                                     w=35,
                                     h=70,
                                     x=random.randint(0, SCREEN_WIDTH - 35),
                                     y=random.randint((SCREEN_HEIGHT >> 1) - 140, SCREEN_HEIGHT >> 1),
                                     velocity=random.randint(20, 30),
                                     debug=True))

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

    def shot(self, x: int, y: int):
        for z in self.entities:
            if 0 < x - z.x < z.w * z.scale and 0 < y - z.y < z.h * z.scale:
                screams.play()
                z.is_dead = True
                self.Kill += 1
                break


def render_end_screen(entities: EntitySystem):
    game_over_txt = pygame.font.Font(None, 40).render("GAME OVER", True, pygame.Color('white'))
    retry_txt = pygame.font.Font(None, 35).render("Press R to Retry", True, pygame.Color('white'))
    quit_txt = pygame.font.Font(None, 35).render("Press Q to Quit", True, pygame.Color('white'))
    score_txt = pygame.font.Font(None, 35).render("SCORE: " + str(entities.Kill), True, pygame.Color('White'))

    screen.blit(game_over_txt, ((SCREEN_WIDTH - game_over_txt.get_width()) // 2,
                                (SCREEN_HEIGHT - game_over_txt.get_height()) // 2 - SCREEN_HEIGHT // 15))
    screen.blit(score_txt, ((SCREEN_WIDTH - score_txt.get_width()) // 2,
                            (SCREEN_HEIGHT - score_txt.get_height()) // 2 - SCREEN_HEIGHT // 7))

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
    # BGM Start
    bgm.play(-1)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                gun_shot.play()
                pos = pygame.mouse.get_pos()
                entities.shot(pos[0], pos[1])

        # count = (count + 1) % len(sprite_list)

        # Prompt end-game screen
        timer -= delta_t
        if timer <= 0:
            timer = 0
            get_event = False
            render_end_screen(entities)
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
