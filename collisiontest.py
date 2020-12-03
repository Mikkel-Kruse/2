def collision_test(rect, tiles): # rect = palyer rect. tiles = list of tile
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile): # if player collide with tile
            hit_list.append(tile) # add it to hit list
    return hit_list