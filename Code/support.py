import pygame
from csv import reader
from settings import tile_x, tile_y


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_x)
    tile_num_y = int(surface.get_size()[0] / tile_y)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_x
            y = row * tile_y
            new_surf = pygame.Surface((tile_x, tile_y), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, tile_x, tile_y))
            cut_tiles.append(new_surf)
    return cut_tiles
