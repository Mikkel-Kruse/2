import pygame


class Screen:

    def __init__(self):
        self.caption = pygame.display.set_caption('Storytelling')
        self.window_size = (600, 400)
        self.screen = pygame.display.set_mode(self.window_size, 0, 32)
        self.display = pygame.Surface((300,200))
