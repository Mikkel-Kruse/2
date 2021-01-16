import pygame, sys, random
from speech_recognizer.speech_recognizer import act_on_voice_command
from pygame.locals import *
from opdatermap import generate_chunk
from changeaction import change_action
from collision_move import move
from setup.setup_screen import Screen
import speech_recognition as sr
from setup.setup_sound import Sound
from setup.setup_player import Player
from move.setup_move import MovePlayer
import concurrent.futures
import multiprocessing
from move.loop_make_player_move_controle import move_player_controle
from move.loop_make_player_move_physics import move_player_physics
from game_animations.backgronud import loop_background
from game_animations.player_animations import loop_player_animations
from game_animations.infinit_game import loop_infinit_game
from loadani import load_animation

#mic = sr.Microphone()
#speech = sr.Recognizer()
clock = pygame.time.Clock()

screen = Screen()
sound = Sound()
move_player = MovePlayer()
player = Player()

animation_database = {}
animation_frames = {}
animation_database['run'], animation_frames = load_animation('player_animations/run', [7, 7], animation_frames)
animation_database['idle'], animation_frames = load_animation('player_animations/idle', [7, 7, 40], animation_frames)

player_action = 'idle'
player_frame = 0
player_flip = False

#grass_sound_timer = 0


#grass_img = pygame.image.load('utils/grass2.png')
#dirt_img = pygame.image.load('utils/dirt2.png')
#plant_img = pygame.image.load('utils/plant.png').convert()
#plant_img.set_colorkey((255,255,255))

#tile_index = {1:grass_img, 2:dirt_img, 3:plant_img}


player_man_rect = pygame.Rect(100, 100, 5, 13)

#background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30,40,400]], [0.5, [30, 40, 40, 400]], [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

while True:
    screen.display.fill((146, 244, 255))

    if sound.grass_sound_timer > 0:
        sound.grass_sound_timer -= 1

    screen.scroll[0] += (player_man_rect.x-screen.scroll[0]-152)/20 # makes the scroll delayed and follow player in x
    screen.scroll[1] += (player_man_rect.y-screen.scroll[1]-106)/20

    loop_background(screen)

    # opdatere infinite game og gemmer det i tile_rects
    tile_rects = loop_infinit_game(screen)

    #
    player_man_movement = [0, 0]

    move_player_physics(move_player, player_man_movement)

    #loop_player_animations(change_action, player)


    if player_man_movement[0] > 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = False
    if player_man_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_man_movement[0] < 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = True
                                       
    player_man_rect, collisions = move(player_man_rect, player_man_movement, tile_rects)

    if collisions['bottom']:
        move_player.player_y_momentum = 0
        move_player.air_timer = 0
        if player_man_movement[0] != 0:
            if sound.grass_sound_timer == 0:
                sound.grass_sound_timer = 30
                random.choice(sound.grass_sounds).play()
    else:
        move_player.air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_man_img = animation_frames[player_img_id]
    screen.display.blit(pygame.transform.flip(player_man_img,player_flip, False), (player_man_rect.x - screen.scroll[0], player_man_rect.y - screen.scroll[1]))

    move_player_controle(move_player)

    screen.screen.blit(pygame.transform.scale(screen.display, screen.window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)

