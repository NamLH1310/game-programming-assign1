import string
import pygame

#Base Class for sprite sheet uses
class SpriteSheet:
    
    index:int #index of sprite list
    file_name:string # path to sprite
    sprite_sheet:pygame.Surface # base sprite sheet
    sprite_list:any #list of all sub sprite
    
# Zombie sprite
class Zombie(SpriteSheet):
    
    def get_sprite(self,w,h,index):
        '''
        Split sprite form from zombie.png include 8 sprite
        '''
        sprite=pygame.Surface((93.1,81.6))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0,0),(558.8+97*index,260.8,93.1,81.6))
        scale_sprite=pygame.transform.scale(sprite,(w,h))
        
        return scale_sprite
        
    
    def __init__(self,filename,w,h) -> None:
        '''
        Set base data for object zombie
        '''
        self.index=0
        self.file_name=filename
        self.sprite_sheet=pygame.image.load(self.file_name).convert()
        self.sprite_list=[]
        '''
        Get the sub sprite from sprite sheet
        '''
        for i in range(8):
            self.sprite_list+=[self.get_sprite(w,h,i)]
        
    def draw(self,die:bool,fps:int):
        '''
        Return base sprite 
        loop if shot(die==true), all loop done in 1s
        '''
        if die:
            index+=1
        num=index/(fps/8)
        
        if (num>=len(self.sprite_list)):
            return
        
        return self.sprite_list[num]
    
    def draw_demo(self):
        '''
        Demo of object
        '''
        rv=list.copy(self.sprite_list)
        return rv
    
# Base class for All cursor related object
class Aim(SpriteSheet):
    
    def __init__(self,filename):
        '''
        Base Data for Aim only carry path and single sprite due to no sprite sheet import
        '''
        self.file_name=filename
        self.sprite_sheet=pygame.image.load(self.file_name)
    
    def draw(self,w,h):
        '''
        Draw from base sprite but transform if w,h equal 0
        '''
        if w==0 and h==0 :
            w=self.sprite_sheet.get_width
            h=self.sprite_sheet.get_height
        
        sprite=pygame.transform.scale(self.sprite_sheet,(w,h))
        return sprite