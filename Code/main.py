import pygame, sys
from settings import *
from level import Level
from Overworld import Overworld
from main_menu import main_menu


class Game:
    def __init__(self):
        self.max_level = 1
        self.current_level = 0
        self.main_menu = main_menu(self.max_level, self.current_level, screen, self.create_overworld)
        self.status = 'main_menu'

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.create_level)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level, self.create_main_menu)
        self.status = 'overworld'

    def create_main_menu(self, current_level, max_level):
        self.main_menu = main_menu(current_level, max_level, screen, self.create_overworld)
        self.status = 'main_menu'

    def run(self):
        if self.status == 'main_menu':
            self.main_menu.run()
        elif self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        bg = pygame.image.load('../Graphics/Textures/bg.png').convert()
        screen.blit(bg, (0,0))

        game.run()

        pygame.display.update()
        clock.tick(60)