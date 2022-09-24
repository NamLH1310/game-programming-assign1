import pygame
from pygame import Surface


class Zombie:
    def __init__(self,
                 screen: pygame.Surface,
                 filename: str,
                 w: int,
                 h: int,
                 x: int,
                 y: int,
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

        self.screen = screen
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.hitbox_x= w/5
        self.hitbox_y= h/6
        self.hitbox_w= w/2
        self.hitbox_h= h/1.18
        self.index = 0
        self.debug = debug
        self.filename = filename
        self.sprite_sheet = pygame.image.load(self.filename).convert()
        self.sprite_list = [self.get_sprite(w, h, i) for i in range(8)]

    def get_sprite(self, w: int, h: int, index: int) -> pygame.Surface:
        """
        Split sprite form from zombie.png include 8 sprite
        """
        sprite = pygame.Surface((93.1, 81.6))

        # sprite.fill((0,0,0))

        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (558 + 97 * index, 260, 93, 81))
        return pygame.transform.scale(sprite, (w, h))

    def draw(self, die: bool, fps: int) -> None:
        """
        Return base sprite
        loop if shot(die==true), all loop done in 1s
        """
        if die:
            self.index += 1

        num = self.index // (fps // 8)

        if num >= len(self.sprite_list):
            return None

        self.screen.blit(self.sprite_list[num], (self.x, self.y))

        if self.debug:
            self.draw_hit_box()

    def get_sprites(self) -> list[pygame.Surface]:
        """
        Demo of object
        """
        return self.sprite_list

    def draw_hit_box(self):
        pygame.draw.rect(
            self.screen, (0, 0, 255),
            pygame.Rect(
                self.x,
                self.y,
                self.w,
                self.h
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
