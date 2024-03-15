import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size_x, size_y, x, y):
        super().__init__()
        self.image = pygame.Surface((size_x, size_y))
        self.rect = self.image.get_rect(topleft = (x,y))


class StaticTile(Tile):
    def __init__(self, size_x, size_y, x, y, surface):
        super().__init__(size_x, size_y, x, y)
        self.image = surface
