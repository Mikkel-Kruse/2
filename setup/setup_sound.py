import pygame

class Sound:

    def __init__(self):
        self.sound_delay = pygame.mixer.pre_init(44100, -16, 2, 512)  # changing the sound
        self.sound_initialize = pygame.init()
        self.sound_channel = pygame.mixer.set_num_channels(64)
        self.jump_sound = pygame.mixer.Sound('utils/jump.wav')
        self.jump_volume = self.jump_sound.set_volume(0.4)
        self.grass_sounds = [pygame.mixer.Sound('utils/grass_0.wav'), pygame.mixer.Sound('utils/grass_1.wav')]
        self.grass0_volume = self.grass_sounds[0].set_volume(0.2)
        self.grass1_volume = self.grass_sounds[1].set_volume(0.2)
        self.game_music = pygame.mixer.music.load('utils/music.wav')
        self.game_music_loop = pygame.mixer.music.play(-1)
        self.grass_sound_timer = 0