import pygame
from tiles import StaticTile
from random import randint


class Enemy(StaticTile):
    def __init__(self, size_x, size_y, x, y, path):
        super().__init__(size_x, size_y, x, y, path)
        self.speed = randint(3, 5)
        self.orientation = 'left'

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0 and self.orientation == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
            self.orientation = 'right'
        elif self.speed < 0 and self.orientation == 'right':
            self.image = pygame.transform.flip(self.image, True, False)
            self.orientation = 'left'

    def reverse(self):
        self.speed *= -1

    def update(self):
        self.move()
        self.reverse_image()