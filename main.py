import pygame
from pygame import mixer
from script.fighter import Fighter
from script.ui import *
import colors
import chara_attr

mixer.init()
pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("God Bless You DUEL!")

clock = pygame.time.Clock()
FPS = 60

intro_count = 4 
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player score. [P1, P2]
round_over = False 
ROUND_OVER_COOLDOWN = 2000

pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

gbs_atk_fx = pygame.mixer.Sound("assets/audio/gbs_atk_01.mp3")
pygame.mixer.music.set_volume(0.5)
zeus_atk_01_fx = pygame.mixer.Sound("assets/audio/zeus_atk_01.wav")
pygame.mixer.music.set_volume(0.5)
zeus_atk_02_fx = pygame.mixer.Sound("assets/audio/zeus_atk_02.wav")
pygame.mixer.music.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/hit.mp3")
pygame.mixer.music.set_volume(0.75)

arena_bg = pygame.image.load("assets/bg/Arena.jpg").convert_alpha()

player_1_sheet = pygame.image.load("assets/sprite_sheets/SOULMEN_GBS.png").convert_alpha()
player_2_sheet = pygame.image.load("assets/sprite_sheets/ZEUS.png").convert_alpha()

health_P1_img = pygame.image.load("assets/icon/health_P1.png").convert_alpha()
health_P2_img = pygame.image.load("assets/icon/health_P2.png").convert_alpha()

victory_img = pygame.image.load("assets/icon/victory.png").convert_alpha()
game_start_img = pygame.image.load("assets/icon/game_start.png").convert_alpha()
game_reset_img = pygame.image.load("assets/icon/game_reset.png").convert_alpha()
#transparency_victory = pygame.transform.scale(victory_img.convert_alpha)

count_font = pygame.font.Font("assets/font/OptimusPrincepsSemiBold.ttf", 80)
score_font = pygame.font.Font("assets/font/OptimusPrincepsSemiBold.ttf", 30)

#transparency = 120
#set_surface = pygame.surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

#def draw_transparency_victory():
#    pygame.draw.rect(set_surface ,(255, 0, 0, transparency), [100, 100, 200, 100])
#    set_surface.set_alpha(transparency)
#    set_surface.blit(transparency_victory, (0, 0))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    scaled_bg = pygame.transform.scale(arena_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

chara_1 = chara_attr.SOULMEN_GBS_ANIMATION_STEP
chara_2 = chara_attr.ZEUS_ANIMATION_STEP

player_1 = Fighter(1 , 200, 600, chara_attr.test_player_1_data, player_1_sheet, chara_1, 10 ,15, gbs_atk_fx, gbs_atk_fx, hit_fx)
player_2 = Fighter(2 , 1300, 600, chara_attr.test_player_2_data, player_2_sheet, chara_2, 10, 30, zeus_atk_01_fx, zeus_atk_02_fx, hit_fx)

run = True
while run:

    clock.tick(FPS)

    draw_bg()

   # screen.blit(health_P1_img,(-25, -15))
   # screen.blit(health_P2_img,(1150, -15))

    draw_health_bar(health_P1_img, -25, -15, player_1.health, 20, 20, screen, colors.white, colors.dark_brown, colors.orange)
    draw_health_bar(health_P2_img, 1150, -15, player_2.health, 1180, 20, screen, colors.white, colors.dark_brown,  colors.orange)
    draw_text(str(score[0]), score_font, colors.white, 45, 52)
    draw_text(str(score[1]), score_font, colors.white, 1540, 52)

    if intro_count <= 0:
        player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
        player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
    else:
        screen.blit(game_start_img, ( 0, -100))
        draw_text(str(intro_count), count_font, colors.white, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.2)
        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            print(intro_count)

    player_1.update()
    player_2.update() 

    player_2.draw(screen)
    player_1.draw(screen)
   

    if round_over == False:
        if player_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif player_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img,(0, -100))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            player_1 = Fighter(1 , 200, 600, chara_attr.test_player_1_data, player_1_sheet, chara_1, 10 ,15, gbs_atk_fx, gbs_atk_fx, hit_fx)
            player_2 = Fighter(2 , 1300, 600, chara_attr.test_player_2_data, player_2_sheet, chara_2, 10, 30, zeus_atk_01_fx, zeus_atk_02_fx, hit_fx)

#    if score[0] == 4 or score[1] == 4:
#        if score[0] == 4:
#            score[0] = 0
#            score[1] = 0
#        elif score[1] == 4:
#            score[0] = 0
#           score[1] = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()