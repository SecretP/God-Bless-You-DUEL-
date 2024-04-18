import pygame
from sys import exit

screen_width = 800
screen_height = 600

pygame.init()
screen = pygame.display.set_mode((1600,960))
pygame.display.set_caption('God Bless You DUEL!')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None,50)

#test_surface = pygame.image.load('asset/testloadimg.jpg')
arena_bg = pygame.image.load('assets/bg/Arena.jpg')
text_surface = test_font.render('Start',False,'Black')
zeus_surface = pygame.image.load('assets/Zeus move/zeus move_0000.png')
zeus_x_pos = 1400

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(arena_bg,(0,0))
    screen.blit(text_surface,(800,200))
    screen.blit(zeus_surface,(0,-200))
    zeus_x_pos -=1
 

    pygame.display.update()
    clock.tick(60)