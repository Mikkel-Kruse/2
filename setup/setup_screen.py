import pygame


class Screen:

    def __init__(self):
        self.caption = pygame.display.set_caption('Storytelling')
        self.window_size = (600, 400)
        self.screen = pygame.display.set_mode(self.window_size, 0, 32)
        self.display = pygame.Surface((300,200))
        self.background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30,40,400]], [0.5, [30, 40, 40, 400]], [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]
        self.scroll = [0,0]
        self.chunk_size = 8
        self.game_map = {}
        self.tile_rects = []
        self.grass_img = pygame.image.load('utils/grass2.png')
        self.dirt_img = pygame.image.load('utils/dirt2.png')
        self.plant_img = pygame.image.load('utils/plant.png').convert()
        self.plant_img.set_colorkey((255,255,255))
        self.tile_index = {1:self.grass_img, 2:self.dirt_img, 3:self.plant_img}
