import pygame, sys, numpy
from settings import *
from level import Level

#Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        bg = pygame.image.load('../Graphics/Textures/bg.png')
        screen.blit(bg, (0,0))

        level.run()

        pygame.display.update()
        clock.tick(60)