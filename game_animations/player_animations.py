import pygame
from changeaction import change_action
from setup.setup_player import Player
from move.loop_make_player_move_physics import move_player_physics

player = Player()
player_action = 'idle'
player_frame = 0
player_flip = False

player_man_movement = [0,0]
#move_player_physics(player_man_movement)

def loop_player_animations(change_action, player_action, player_frame, player_flip):
    move_player_physics(player_man_movement)
    if player_man_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    if player_man_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')
    if player_man_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True

