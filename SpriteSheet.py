from dataclasses import dataclass

import pygame


# Base Class for sprite sheet uses
@dataclass
class SpriteSheet:
    index: int  # index of sprite list
    file_name: str  # path to sprite
    sprite_sheet: pygame.Surface  # base sprite sheet
    sprite_list: list[pygame.Surface]  # list of all sub sprite


# Zombie sprite
@dataclass
class Zombie(SpriteSheet):

    def get_sprite(self, w: int, h: int, index: int):
        """
        Split sprite form from zombie.png include 8 sprite
        """
        sprite = pygame.Surface((93.1, 81.6))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (558.8 + 97 * index, 260.8, 93.1, 81.6))
        scale_sprite = pygame.transform.scale(sprite, (w, h))

        return scale_sprite

    def __init__(self, filename: str, w: int, h: int) -> None:
        """
        Set base data for object zombie
        """
        self.index = 0
        self.file_name = filename
        self.sprite_sheet = pygame.image.load(self.file_name).convert()
        '''
        Get the sub sprite from sprite sheet
        '''
        self.sprite_list = [self.get_sprite(w, h, i) for i in range(8)]

    def draw(self, die: bool, fps: int) -> None | pygame.Surface:
        """
        Return base sprite
        loop if shot(die==true), all loop done in 1s
        """
        if die:
            self.index += 1

        num = self.index // (fps // 8)

        if num >= len(self.sprite_list):
            return None

        return self.sprite_list[num]

    def draw_demo(self) -> list[pygame.Surface]:
        """
        Demo of object
        """
        return list.copy(self.sprite_list)


# Base class for All cursor related object
class Aim(SpriteSheet):

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
