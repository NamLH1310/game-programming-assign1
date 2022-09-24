from dataclasses import dataclass
from random import randbytes, randint, random
from re import X
from tempfile import tempdir
from typing import Tuple

import pygame
from pygame import Surface

from constants import FPS


class Zombie:
    def __init__(self,
                 filename: str,
                 w: int,
                 h: int,
                 x: int,
                 y: int,
                 debug: bool = False) -> None:
        """
        Set base data for object zombie
        """
        assert type(filename) is str
        assert type(w) is int
        assert type(h) is int
        assert type(x) is int
        assert type(y) is int
        assert type(debug) is bool

        self.x=x
        self.y=y
        self.w = w
        self.h = h
        self.hitbox_x= x+w/5
        self.hitbox_y= y+h/6
        self.hitbox_w= w/2
        self.hitbox_h= h/1.18
        self.die=False
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

    def draw(self, fps: int) -> None:
        """
        Return base sprite
        loop if shot(die==true), all loop done in 1s
        """
        if self.die:
            self.index += 1

        num = self.index // (fps // 12)

        if num >= len(self.sprite_list):
            return None

        if self.debug:
            self.draw_hit_box(num)

        return self.sprite_list[num]

    def get_sprites(self) -> list[pygame.Surface]:
        """
        Demo of object
        """
        rv=list.copy(self.sprite_list)
        
        return rv
    def draw_hit_box(self, index:int):
        pygame.draw.rect(
            self.sprite_list[index], (255, 0, 0),
            pygame.Rect(
                self.hitbox_x-self.x,
                self.hitbox_y-self.y,
                self.hitbox_w,
                self.hitbox_y
            ),
            3
        )
    def setHitBox(self,x:int,y:int):
        self.x=x
        self.y=y
        self.hitbox_x=x+self.w/5
        self.hitbox_y=y+self.h/6


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

class Horde:
    zombies:list[Zombie]
    cors:list[Tuple[int]]
    height:int
    width:int
    clear:int
    
    def __init__(self, num:int, width:int, height:int, debug:bool) -> None:
        self.width=width
        self.height=height
        self.zombies=list()
        self.cors=list()
        for i in range(num):
            self.zombies.append(Zombie('./image/zombie.png',width,height,0,0,debug))
            self.cors.append((0,0))
        
    def _check_(self,sw,sh ,x:int ,y:int):
        for i in self.cors:
            disX=abs(x-i[0])
            disY=abs(y-i[1])
            if disX<self.width//2 or disY<self.height//2:
                return False
        return True
        
    def randomSpawn(self, screenWidth:int,screenHeight:int,dis:int):
        self.clear=0
        i=0
        counter=0
        
        for j in range(len(self.zombies)):
            self.zombies[j].index=0
        while(i<len(self.cors)):
            x=round((screenWidth-dis-self.width)*random()+dis)
            y=round((screenHeight-dis-self.height)*random()+dis)
            if self._check_(screenWidth,screenHeight,x,y):
                self.cors.__setitem__(i,(x,y))
                self.zombies[i].setHitBox(x,y)
                i+=1
            elif counter>5:
                continue
            else:
                counter+=1
    
    def spawn(self,canvas:pygame.Surface):
        for i in range(len(self.cors)):
            zombie=self.zombies[i].draw(FPS)
            if zombie is None:
                continue
            canvas.blit(zombie,self.cors[i])
            
    def checkClear(self,screenWidth:int,screenHeight:int,dis:int):   
        if(self.clear==len(self.zombies)):
            self.clear=0
            self.randomSpawn(screenWidth,screenHeight,dis)
    def reset(self,index:int):
        self.zombies[index].index=0
    
    def shoot(self, x,y):
        clear+=1
        pass