import pygame, sys, random
from speech_recognizer.speech_recognizer import SpeechCommander
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


class GameController:

    def __init__(self):
        self.queue = multiprocessing.Queue()
        self.speech_commander = SpeechCommander(self.queue)
        self.screen = Screen()
        self.sound = Sound()
        self.move_player = MovePlayer()
        self.player = Player()
        self.animation_database = {}
        self.animation_frames = {}
        self.clock = pygame.time.Clock()
        self.setup_game()
        self.speech_commander.start_commander()

    def setup_game(self):
        self.animation_database['run'], self.animation_frames = load_animation('player_animations/run', [7, 7], self.animation_frames)
        self.animation_database['idle'], self.animation_frames = load_animation('player_animations/idle', [7, 7, 40], self.animation_frames)

    def run_game(self):
        player_man_rect = pygame.Rect(100, 100, 5, 13)
        while True:
            self.screen.display.fill((146, 244, 255))

            if self.sound.grass_sound_timer > 0:
                self.sound.grass_sound_timer -= 1

            self.screen.scroll[0] += (player_man_rect.x - self.screen.scroll[0] - 152) / 20  # makes the scroll delayed and follow player in x
            self.screen.scroll[1] += (player_man_rect.y - self.screen.scroll[1] - 106) / 20

            loop_background(self.screen)

            # opdatere infinite game og gemmer det i tile_rects
            tile_rects = loop_infinit_game(self.screen)

            #
            player_man_movement = [0, 0]

            move_player_physics(self.move_player, player_man_movement)

            # loop_player_animations(change_action, player)

            if player_man_movement[0] > 0:
                self.player.player_action, self.player.player_frame = change_action(self.player.player_action, self.player.player_frame, 'run')
                self.player.player_flip = False
            if player_man_movement[0] == 0:
                self.player.player_action, self.player.player_frame = change_action(self.player.player_action, self.player.player_frame, 'idle')
            if player_man_movement[0] < 0:
                self.player.player_action, self.player.player_frame = change_action(self.player.player_action, self.player.player_frame, 'run')
                self.player.player_flip = True

            player_man_rect, collisions = move(player_man_rect, player_man_movement, tile_rects)

            if collisions['bottom']:
                self.move_player.player_y_momentum = 0
                self.move_player.air_timer = 0
                if player_man_movement[0] != 0:
                    if self.sound.grass_sound_timer == 0:
                        self.sound.grass_sound_timer = 30
                        random.choice(self.sound.grass_sounds).play()
            else:
                self.move_player.air_timer += 1

            self.player.player_frame += 1
            if self.player.player_frame >= len(self.animation_database[self.player.player_action]):
                self.player.player_frame = 0
            player_img_id = self.animation_database[self.player.player_action][self.player.player_frame]
            player_man_img = self.animation_frames[player_img_id]
            self.screen.display.blit(pygame.transform.flip(player_man_img, self.player.player_flip, False),
                                (player_man_rect.x - self.screen.scroll[0], player_man_rect.y - self.screen.scroll[1]))

            move_player_controle(self.move_player)

            self.screen.screen.blit(pygame.transform.scale(self.screen.display, self.screen.window_size), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

            if not self.queue.empty():
                text = self.queue.get()
                print(text)
                if 'walk' in text:
                    self.move_player.moving_right = True
                if 'stop' in text:
                    self.move_player.moving_right = False
                if 'jump' in text:
                    self.move_player.player_y_momentum = -10


if __name__ == '__main__':
    game_controller = GameController()
    game_controller.run_game()