import pygame

       


def draw_health_bar(frame, frame_x, frame_y, health, x, y, surface, color_1, color_2, color_3):
    ratio = health / 100
    pygame.draw.rect(surface, color_1, (x - 4, y - 3, 408 , 36))
    pygame.draw.rect(surface, color_2, (x, y , 400, 30))
    pygame.draw.rect(surface, color_3, (x, y, 400 * ratio, 30))

    surface.blit(frame, (frame_x, frame_y))