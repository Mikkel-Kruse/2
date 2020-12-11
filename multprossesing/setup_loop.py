import pygame, sys, random
from speech_recognizer.speech_recognizer import act_on_voice_command
from pygame.locals import *
from opdatermap import generate_chunk
from changeaction import change_action
from collision_move import move
from threading import Thread
from setup.setup_screen import Screen
import speech_recognition as sr
import multiprocessing
from multprossesing.setup_all import setup_all

setup_all()
screen = Screen()

def setup_loop():
    while True:
        screen.display.fill((146, 244, 255))


        if grass_sound_timer > 0:
            grass_sound_timer -= 1

        scroll[0] += (player_man_rect.x - scroll[0] - 152) / 20  # makes the scroll delayed and follow player in x
        scroll[1] += (player_man_rect.y - scroll[1] - 106) / 20

        pygame.draw.rect(screen.display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
        for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0],
                                   background_object[1][1] - scroll[1] * background_object[0], background_object[1][2],
                                   background_object[1][3])
            if background_object[0] == 0.5:
                pygame.draw.rect(screen.display, (14, 222, 150), obj_rect)
            else:
                pygame.draw.rect(screen.display, (9, 91, 85), obj_rect)

        tile_rects = []
        for y in range(3):
            for x in range(4):
                target_x = x - 1 + int(round(scroll[0] / (
                            chunk_size * 16)))  # calculating what chunk the top left of the screen is, adding the x gives you all chuncks visible on the screen
                target_y = y - 1 + int(round(scroll[1] / (chunk_size * 16)))
                target_chunk = str(target_x) + ';' + str(target_y)
                if target_chunk not in game_map:
                    game_map[target_chunk] = generate_chunk(target_x, target_y)  # generate chunck if they dont exist yet
                for tile in game_map[target_chunk]:
                    screen.display.blit(tile_index[tile[1]], (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]))
                    if tile[1] in [1, 2]:
                        tile_rects.append(
                            pygame.Rect(tile[0][0] * 16, tile[0][1] * 16, 16, 16))  # adding til 1 and 2 to collision

        player_man_movement = [0, 0]
        if moving_right:
            player_man_movement[0] += 2
        if moving_left:
            player_man_movement[0] -= 2
        player_man_movement[1] += player_y_momentum
        player_y_momentum += 0.2
        if player_y_momentum > 3:
            player_y_momentum = 3

        if player_man_movement[0] > 0:
            player_action, player_frame = change_action(player_action, player_frame, 'run')
            player_flip = False
        if player_man_movement[0] == 0:
            player_action, player_frame = change_action(player_action, player_frame, 'idle')
        if player_man_movement[0] < 0:
            player_action, player_frame = change_action(player_action, player_frame, 'run')
            player_flip = True

        player_man_rect, collisions = move(player_man_rect, player_man_movement, tile_rects)

        if collisions['bottom']:
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
        screen.display.blit(pygame.transform.flip(player_man_img, player_flip, False),
                            (player_man_rect.x - scroll[0], player_man_rect.y - scroll[1]))

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

        screen.screen.blit(pygame.transform.scale(screen.display, screen.window_size), (0, 0))
        pygame.display.update()
        clock.tick(60)
