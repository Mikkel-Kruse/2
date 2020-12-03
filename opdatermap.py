import pygame, sys, os, random

chunk_size = 8

def generate_chunk(x,y): # generates infinit map
    chunk_data = []
    for y_pos in range(chunk_size): # The tiles posistion in the chuncks
        for x_pos in range(chunk_size):
            target_x = x * chunk_size + x_pos # The positsion of the specifick tile
            target_y = y * chunk_size + y_pos
            tile_type = 0
            if target_y > 10:
                tile_type = 2
            elif target_y == 10:
                tile_type = 1
            elif target_y == 9:
                if random.randint(1,5) == 1:
                    tile_type = 3
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data