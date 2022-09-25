import pygame
from pygame import Surface

from constants import FPS, SCREEN_HEIGHT


class Zombie(pygame.sprite.Sprite):
    def __init__(self,
                 screen: pygame.Surface,
                 filename: str,
                 w: int,
                 h: int,
                 x: int,
                 y: int,
                 velocity: int,
                 debug: bool = False) -> None:
        """
        Set base data for object zombie
        """
        assert type(screen) is Surface
        assert type(filename) is str
        assert type(w) is int
        assert type(h) is int
        assert type(x) is int
        assert type(y) is int
        assert type(debug) is bool

        super().__init__()
        self.num_frames = 0
        self.screen = screen
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.index = 0
        self.debug = debug
        self.filename = filename
        self.scale = 2
        self.velocity = velocity
        self.is_dead = False
        self.sprite_sheet = pygame.image.load(self.filename).convert()
        self.sprite_list = list[Surface]([
            self.get_sprite(0, 188, self.w, self.h),
            self.get_sprite(200, 188, self.w, self.h),
            self.get_sprite(300, 188, self.w, self.h),
            self.get_sprite(390, 188, self.w, self.h),
            self.get_sprite(485, 188, self.w, self.h),
            self.get_sprite(590, 188, self.w, self.h),
        ])

    def get_sprite(self, x: int, y: int, w: int, h: int) -> Surface:
        """
        Split sprite form from zombie.png include 8 sprite
        """
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return pygame.transform.scale(sprite, (w * self.scale, h * self.scale))

    def draw(self) -> None:
        """
        Return base sprite
        loop if shot(die==true), all loop done in 1s
        """
        self.num_frames += 1
        if self.num_frames >= FPS >> 1:
            self.num_frames = 0
            self.index = (self.index + 1) % len(self.sprite_list)
            if self.y < SCREEN_HEIGHT - self.h:
                self.y += self.velocity

        if self.y >= SCREEN_HEIGHT - self.h or self.is_dead:
            self.is_dead = True
            self.kill()

        self.screen.blit(self.sprite_list[self.index], (self.x, self.y))

        if self.debug:
            self.draw_hit_box()

    def draw_hit_box(self):
        pygame.draw.rect(
            self.screen, (0, 0, 255),
            pygame.Rect(
                self.x,
                self.y,
                self.w * self.scale,
                self.h * self.scale
            ),
            3
        )


# Base class for All cursor related object
class Aim:
    def __init__(self, filename: str):
        """
        Base Data for Aim only carry path and single sprite due to no sprite sheet import
        """
        self.sprite_sheet = pygame.image.load(filename)

    def draw(self, w: int, h: int) -> pygame.Surface:
        """
        Draw from base sprite but transform if w,h equal 0
        """
        if w == 0 and h == 0:
            w = self.sprite_sheet.get_width
            h = self.sprite_sheet.get_height

        return pygame.transform.scale(self.sprite_sheet, (w, h))
