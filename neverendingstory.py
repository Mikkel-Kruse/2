from typing import Any, Union

import pygame, sys, os, random
import speech_recognition as sr


r = sr.Recognizer()
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512) # changing the sound
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Storytelling')

window_size = (600, 400)

screen = pygame.display.set_mode(window_size, 0, 32)

display = pygame.Surface((300,200))

moving_right = False
moving_left = False
player_y_momentum = 0
air_timer = 0

scroll = [0, 0]

chunk_size = 8

from opdatermap import generate_chunk


global animation_frames
animation_frames = {}

#from loadani import load_animation

def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255, 255, 255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

from changeaction import change_action


animation_database = {}

animation_database['run'] = load_animation('player_animations/run',[7, 7])
animation_database['idle'] = load_animation('player_animations/idle',[7, 7, 40])

game_map = {}


player_action = 'idle'
player_frame = 0
player_flip = False

grass_sound_timer = 0


grass_img = pygame.image.load('grass2.png')
dirt_img = pygame.image.load('dirt2.png')
plant_img = pygame.image.load('plant.png').convert()
plant_img.set_colorkey((255,255,255))

tile_index = {1:grass_img, 2:dirt_img, 3:plant_img}


jump_sound = pygame.mixer.Sound('jump.wav')
jump_sound.set_volume(0.4)
grass_sounds = [pygame.mixer.Sound('grass_0.wav'), pygame.mixer.Sound('grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)

player_man_rect = pygame.Rect(100, 100, 5, 13)

background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30,40,400]], [0.5, [30, 40, 40, 400]], [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]


from collision_move import move


while True:
    display.fill((146, 244, 255))

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    scroll[0] += (player_man_rect.x-scroll[0]-152)/20 # makes the scroll delayed and follow player in x
    scroll[1] += (player_man_rect.y-scroll[1]-106)/20

    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0], background_object[1][1] - scroll[1] * background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(display,(9, 91, 85), obj_rect)


    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0]/(chunk_size*16))) # calculating what chunk the top left of the screen is, adding the x gives you all chuncks visible on the screen
            target_y = y - 1 + int(round(scroll[1]/(chunk_size*16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x, target_y) # generate chunck if they dont exist yet
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
                if tile[1] in [1,2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16)) # adding til 1 and 2 to collision


    player_man_movement = [0, 0]
    if moving_right == True:
        player_man_movement[0] += 2
    if moving_left == True:
        player_man_movement[0] -= 2
    player_man_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    if player_man_movement[0] > 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = False
    if player_man_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_man_movement[0] < 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = True
                                       
    player_man_rect, collisions = move(player_man_rect, player_man_movement, tile_rects)

    if collisions['bottom'] == True:
        player_y_momentum = 0
        air_timer = 0
        if player_man_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_man_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_man_img,player_flip, False), (player_man_rect.x - scroll[0], player_man_rect.y - scroll[1]))




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
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:              
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False



    screen.blit(pygame.transform.scale(display, window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)

