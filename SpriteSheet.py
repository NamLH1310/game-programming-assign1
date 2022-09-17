import string
import pygame

class SpriteSheet:
    index:int
    file_name:string
    sprite_sheet:pygame.Surface
    sprite_list:any
    
class Zombie(SpriteSheet):
    
    def get_sprite(self,w,h,index):
        sprite=pygame.Surface((93.1,81.6))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0,0),(558.8+97*index,260.8,93.1,81.6))
        scale_sprite=pygame.transform.scale(sprite,(w,h))
        
        return scale_sprite
        
    
    def __init__(self,filename,w,h) -> None:
        self.index=0
        self.file_name=filename
        self.sprite_sheet=pygame.image.load(self.file_name).convert()
        self.sprite_list=[]
        for i in range(8):
            self.sprite_list+=[self.get_sprite(w,h,i)]
        print(len(self.sprite_list))
        
    def draw(self,die:bool,fps:int):
        if die:
            index+=1
        num=index/(fps/8)
        if (num>=len(self.sprite_list)):
            return
        return self.sprite_list[num]
    
    def draw_demo(self):
        rv=list.copy(self.sprite_list)
        return rv
    
class Aim(SpriteSheet):
    def __init__(self,filename):
        self.file_name=filename
        self.sprite_sheet=pygame.image.load(self.file_name)
    
    def draw(self,w,h):
        sprite=pygame.transform.scale(self.sprite_sheet,(w,h))
        return sprite