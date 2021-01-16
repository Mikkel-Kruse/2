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
from multprossesing.setup_all import setup_all

st = setup_all()
clock = pygame.time.Clock()
screen = Screen()
sound = Sound()
move_player = MovePlayer()

st

while True:
    screen.display.fill((146, 244, 255))

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    st.scroll[0] += (player_man_rect.x - st.scroll[0] - 152) / 20  # makes the scroll delayed and follow player in x
    st.scroll[1] += (player_man_rect.y - st.scroll[1] - 106) / 20

    pygame.draw.rect(screen.display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
    for background_object in st.background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - st.scroll[0] * background_object[0],
                               background_object[1][1] - st.scroll[1] * background_object[0], background_object[1][2],
                               background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(screen.display, (14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(screen.display, (9, 91, 85), obj_rect)

    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(st.scroll[0] / (
                        st.chunk_size * 16)))  # calculating what chunk the top left of the screen is, adding the x gives you all chuncks visible on the screen
            target_y = y - 1 + int(round(st.scroll[1] / (st.chunk_size * 16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in st.game_map:
                st.game_map[target_chunk] = generate_chunk(target_x, target_y)  # generate chunck if they dont exist yet
            for tile in st.game_map[target_chunk]:
                screen.display.blit(st.tile_index[tile[1]], (tile[0][0] * 16 - st.scroll[0], tile[0][1] * 16 - st.scroll[1]))
                if tile[1] in [1, 2]:
                    tile_rects.append(
                        pygame.Rect(tile[0][0] * 16, tile[0][1] * 16, 16, 16))  # adding til 1 and 2 to collision

    player_man_movement = [0, 0]

    # move_player_physics(move_player)

    if move_player.moving_right:
        player_man_movement[0] += 2
    if move_player.moving_left:
        player_man_movement[0] -= 2
    player_man_movement[1] += move_player.player_y_momentum
    move_player.player_y_momentum += 0.2
    if move_player.player_y_momentum > 3:
        move_player.player_y_momentum = 3

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
        move_player.player_y_momentum = 0
        move_player.air_timer = 0
        if player_man_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(sound.grass_sounds).play()
    else:
        move_player.air_timer += 1

    player_frame += 1
    if player_frame >= len(st.animation_database[player_action]):
        player_frame = 0
    player_img_id = st.animation_database[player_action][player_frame]
    player_man_img = st.animation_frames[player_img_id]
    screen.display.blit(pygame.transform.flip(player_man_img, player_flip, False),
                        (player_man_rect.x - st.scroll[0], player_man_rect.y - st.scroll[1]))

    # move_player_controle()

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

    screen.screen.blit(pygame.transform.scale(screen.display, screen.window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)