import pygame
from setup.setup_screen import Screen

screen = Screen()

def loop_background(screen):
    pygame.draw.rect(screen.display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
    for background_object in screen.background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - screen.scroll[0] * background_object[0], background_object[1][1] - screen.scroll[1] * background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(screen.display,(14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(screen.display,(9, 91, 85), obj_rect)