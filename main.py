import random

from pygame.locals import *

from SpriteSheet import *
from constants import BRIGHT_GREEN, BRIGHT_RED, GREEN, RED, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TIMER, MAX_ZOMBIES, \
    HEALTH, MAX_BULLETS

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
health = HEALTH


# sprite_list = zombie.get_sprites()


class EntitySystem:
    def __init__(self):
        self.entities = set[Zombie]()
        self.deleted_entities = list[Zombie]()
        self.kill_count = 0
        self.shot_count = 0
        self.bullets = MAX_BULLETS
        self.is_reloading = False
        self.num_frames_reload = 0

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
        self.log()
        global health
        self.generate_random_zombie()
        if self.is_reloading:
            self.num_frames_reload += 1
            if self.num_frames_reload >= FPS + (FPS >> 1):
                self.is_reloading = False
                self.num_frames_reload = 0
                self.bullets = MAX_BULLETS

        for z in self.entities:
            if z.is_dead:
                self.deleted_entities.append(z)
            else:
                z.draw()

            if z.reach_destination:
                health -= 10

        for z in self.deleted_entities:
            self.entities.remove(z)

        self.deleted_entities.clear()

    def shot(self, x: int, y: int):
        if self.is_reloading:
            return

        gun_shot.play()
        self.shot_count += 1
        self.bullets -= 1
        if self.bullets == 0:
            self.is_reloading = True

        for z in self.entities:
            if 0 < x - z.x < z.w * z.scale and 0 < y - z.y < z.h * z.scale:
                screams.play()
                z.is_dead = True
                self.kill_count += 1
                break
    
    def reset(self):
        self.entities = set[Zombie]()
        self.deleted_entities = list[Zombie]()
        self.kill_count = 0
        self.shot_count = 0
        self.bullets = MAX_BULLETS
        self.is_reloading = False
        self.num_frames_reload = 0


    def log(self):
        print(f'bullets: {self.bullets}')
        print(f'is reloading: {self.is_reloading}')
        print()


# For bullet
bullet = pygame.image.load("./image/bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet, (bullet.get_width() // 10, bullet.get_height() // 10))
multiply_txt = pygame.font.Font(None, 35).render("X", True, pygame.Color('black'))


def render_end_screen(entities: EntitySystem):
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

    game_over_txt = pygame. \
        font. \
        Font(None, 40). \
        render('GAME OVER', True, pygame.Color('brown'))
    retry_txt = pygame. \
        font. \
        Font(None, 35). \
        render('Retry', True, pygame.Color('black'))
    quit_txt = pygame. \
        font. \
        Font(None, 35). \
        render('Quit', True, pygame.Color('black'))
    score_txt = pygame. \
        font. \
        Font(None, 35). \
        render(f'SCORE: {entities.kill_count}', True, pygame.Color('brown'))
    if entities.shot_count == 0:
        entities.shot_count = 1
    accuracy_txt = pygame. \
        font. \
        Font(None, 35). \
        render(f'ACCURACY: {round((entities.kill_count / entities.shot_count) * 100, None)}%',
               True,
               pygame.Color('brown'))

    screen.blit(game_over_txt, ((SCREEN_WIDTH - game_over_txt.get_width()) // 2,
                                (SCREEN_HEIGHT - game_over_txt.get_height()) // 2 - SCREEN_HEIGHT // 20))
    screen.blit(accuracy_txt, ((SCREEN_WIDTH - accuracy_txt.get_width()) // 2,
                               (SCREEN_HEIGHT - accuracy_txt.get_height()) // 2 - SCREEN_HEIGHT // 10))
    screen.blit(score_txt, ((SCREEN_WIDTH - score_txt.get_width()) // 2,
                            (SCREEN_HEIGHT - score_txt.get_height()) // 2 - SCREEN_HEIGHT // 7))

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
    pygame.display.flip()


def draw(entities: EntitySystem, timer: float) -> None:
    canvas.fill((255, 255, 255))
    canvas.blit(bg, (0, 0))
    canvas.blit(bullet_img, (0.01 * SCREEN_WIDTH, 0.88 * SCREEN_HEIGHT))
    canvas.blit(multiply_txt, (0.03 * SCREEN_WIDTH, 0.92 * SCREEN_HEIGHT))
    canvas.blit(pygame.font.Font(None, 35).render(str(entities.bullets), True, pygame.Color('black')),
                (0.05 * SCREEN_WIDTH, 0.92 * SCREEN_HEIGHT))
    # Zombie
    entities.draw()
    # Mouse
    canvas.blit(target, target_rect)
    canvas.blit(gun, gun_rect)

    # Reattach canvas
    screen.blit(canvas, (0, 0))

    if timer<0:
        timer=0
    timer_text = pygame.font.Font(None, 40).render(f'{round(timer, 2)}', True, pygame.Color('black'))
    screen.blit(timer_text, (5, 5))

    health_text = pygame.font.Font(None, 40).render(f'HEALTH: {health}', True, pygame.Color('red'))

    screen.blit(health_text, (100, 5))
    pygame.display.update()


# Main func
def main() -> None:
    global health
    clock = pygame.time.Clock()
    game_over = False
    # (Delta time since last tick)
    timer: float = TIMER
    delta_t = 0
    entities = EntitySystem()
    # entities.bullets
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
                pos = pygame.mouse.get_pos()
                entities.shot(pos[0], pos[1])

        # Prompt end-game screen
        timer -= delta_t
        if timer < 0 or health <= 0:
            timer = 0
            get_event = False
            render_end_screen(entities)
            pygame.mouse.set_visible(True)
            while not get_event:
                mouse = pygame.mouse.get_pos()

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
                        get_event = True
                        health = HEALTH
                        timer = TIMER
                        clock = pygame.time.Clock()
                        entities.reset()
                        entities.generate_random_zombie()
                        pygame.mouse.set_visible(False)

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
                        game_over = get_event = True

                for event in pygame.event.get():
                    if event.type == QUIT:
                        game_over = get_event = True


        # Displaying remaining time

        # redraw
        draw(entities, timer)
        # pygame.display.update()
        delta_t = clock.tick(FPS) / 1000
        print(delta_t)

    pygame.quit()


if __name__ == '__main__':
    main()
