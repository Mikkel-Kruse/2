import pygame
from opdatermap import generate_chunk
from setup.setup_screen import Screen
# screen = Screen()
grass_img = pygame.image.load('utils/grass2.png')
dirt_img = pygame.image.load('utils/dirt2.png')
plant_img = pygame.image.load('utils/plant.png').convert()
plant_img.set_colorkey((255,255,255))
tile_index = {1:grass_img, 2:dirt_img, 3:plant_img}
#tile_rects = []
def loop_infinit_game(screen):
    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(screen.scroll[0] / (screen.chunk_size * 16)))  # calculating what chunk the top left of the screen is, adding the x gives you all chuncks visible on the screen
            target_y = y - 1 + int(round(screen.scroll[1] / (screen.chunk_size * 16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in screen.game_map:
                screen.game_map[target_chunk] = generate_chunk(target_x, target_y)  # generate chunck if they dont exist yet
            for tile in screen.game_map[target_chunk]:
                screen.display.blit(tile_index[tile[1]], (tile[0][0] * 16 - screen.scroll[0], tile[0][1] * 16 - screen.scroll[1]))
                if tile[1] in [1, 2]:
                    tile_rects.append(pygame.Rect(tile[0][0] * 16, tile[0][1] * 16, 16, 16))  # adding til 1 and 2 to collision
    return tile_rects