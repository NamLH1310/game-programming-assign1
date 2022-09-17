from dataclasses import dataclass

import pygame
from pygame.locals import *
from SpriteSheet import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

##############################################
pygame.init()

# Init screen
canvas=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mouse.set_visible(False)

# Background
bg=Aim('./image/empty_field.png').draw(SCREEN_WIDTH,SCREEN_HEIGHT)

# Cursor param
target=Aim('./image/aim.png').draw(90,90)
gun=Aim('./image/gun.png').draw(250,180)
target_rect=target.get_rect()
gun_rect=gun.get_rect()

# Import char sprite
zombie=Zombie('./image/zombie.png',90,60)
sprite_list=zombie.draw_demo()


def main() -> None:
    count=0 # for testing only
    
    clock = pygame.time.Clock()
    game_over = False

    # game loop
    while not game_over:
        # mouse movement
        (x,y)=pygame.mouse.get_pos()
        gun_rect.center=(x-50,y+50)
        target_rect.center=(x,y)
        
        # single keystroke
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True
            if event.type==pygame.KEYDOWN: #For testing only
                if event.key==pygame.K_SPACE:
                    count=int((count+1)%len(sprite_list))
        clock.tick(FPS)
        # redraw
        canvas.fill((255,255,255))
        canvas.blit(bg,(0,0))
        #Zombie
        canvas.blit(sprite_list[count],(SCREEN_WIDTH-100,SCREEN_HEIGHT-100))
        #Mouse
        canvas.blit(target,target_rect)
        canvas.blit(gun,gun_rect)
        #REattach canvas
        screen.blit(canvas,(0,0))
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
