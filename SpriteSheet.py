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

    def get_sprite(self, w: int, h: int, index: int) -> pygame.Surface:
        """
        Split sprite form from zombie.png include 8 sprite
        """
        sprite = pygame.Surface((93.1, 81.6))
        
        # sprite.fill((0,0,0))
        
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (558.8 + 97 * index, 260.8, 93.1, 81.6))
        scale_sprite = pygame.transform.scale(sprite, (w, h))

        return scale_sprite

    def __init__(self, filename: str, w: int, h: int,debug:bool) -> None:
        """
        Set base data for object zombie
        """
        self.w = w      #   height of sub zombie
        self.h = h
        # self.x        #   coordinate of sub zombie
        # self.y
        self.hitbox_x= w/5
        self.hitbox_y= h/6
        self.hitbox_w= w/2
        self.hitbox_h= h/1.18
        self.index = 0
        self.file_name = filename
        self.sprite_sheet = pygame.image.load(self.file_name).convert()
        '''
        Get the sub sprite from sprite sheet
        '''
        self.sprite_list = [self.get_sprite(w, h, i) for i in range(8)]
        if debug:
            tmp=list.copy(self.sprite_list)
            for i in range(len(tmp)):
                x=tmp[i].get_width()
                y=tmp[i].get_height()
                tmp[i]=self.draw_hitbox(tmp[i],self.hitbox_x,self.hitbox_y,self.hitbox_w,self.hitbox_h)

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
        rv=list.copy(self.sprite_list)
        
        return rv
    
    def draw_hitbox(self,canvas, x, y, w, h):
        return pygame.draw.rect(canvas, (255,0,0), pygame.Rect(x, y, w, h),  3)
    
    pass

    
    # def draw_zombie_rect(self):
    #     self.hitbox_corner = self.sprite_list[0].get_rect()
    #     print(self.hitbox_corner)
    #     color = (255,0,0)
    #     pygame.draw.rect(self.get_sprite(self.w, self.h, 0), color, pygame.Rect(0, 0, 80, 80),  5)


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
