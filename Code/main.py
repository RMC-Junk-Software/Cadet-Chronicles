import pygame, sys
from settings import *
from level import Level
from Game_data import level0, level1, skin1

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level0, skin1, screen)

while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        bg = pygame.image.load('../Graphics/Textures/bg.png').convert()
        screen.blit(bg, (0,0))

        level.run()

        pygame.display.update()
        clock.tick(60)