import pygame, sys, random
from speech_recognizer.speech_recognizer import act_on_voice_command
from pygame.locals import *
from opdatermap import generate_chunk
from changeaction import change_action
from collision_move import move
from threading import Thread
from setup.setup_screen import Screen
import speech_recognition as sr
from setup.setup_sound import Sound
from move.setup_move import MovePlayer
#from move.loop_make_player_move_physics import move_player_physics
#from move.loop_make_player_move_controle import move_player_controle
def setup_all():
    clock = pygame.time.Clock()

    sound = Sound()
    screen = Screen()
    move_player = MovePlayer()

    scroll = [0, 0]

    chunk_size = 8

    global animation_frames
    animation_frames = {}

    # from loadani import load_animation

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

    animation_database = {}

    animation_database['run'] = load_animation('player_animations/run', [7, 7])
    animation_database['idle'] = load_animation('player_animations/idle', [7, 7, 40])

    game_map = {}

    player_action = 'idle'
    player_frame = 0
    player_flip = False

    grass_sound_timer = 0

    grass_img = pygame.image.load('utils/grass2.png')
    dirt_img = pygame.image.load('utils/dirt2.png')
    plant_img = pygame.image.load('utils/plant.png').convert()
    plant_img.set_colorkey((255, 255, 255))

    tile_index = {1: grass_img, 2: dirt_img, 3: plant_img}

    player_man_rect = pygame.Rect(100, 100, 5, 13)

    background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]],
                          [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]
