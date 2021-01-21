import pygame, sys
from pygame.locals import *
from setup.setup_sound import Sound
from move.setup_move import MovePlayer
sound = Sound()


def move_player_controle(move_player):

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_e:
                pygame.mixer.music.play(-1)
            if event.key == K_RIGHT:
                move_player.moving_right = True
            if event.key == K_LEFT:
                move_player.moving_left = True
            if event.key == K_UP:
                if move_player.air_timer < 6:
                    sound.jump_sound.play()
                    move_player.player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                move_player.moving_right = False
            if event.key == K_LEFT:
                move_player.moving_left = False
