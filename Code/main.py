import pygame, sys
from settings import *
from level import Level
from Overworld import Overworld
from main_menu import main_menu


class Game:
    def __init__(self):
        self.current_level = 0
        self.max_level = 3
        self.lives = 2
        self.main_menu = main_menu(self.current_level, self.max_level, screen, self.create_overworld, self.lives)
        self.status = 'main_menu'
        self.level = None

    # Creates a level
    def create_level(self, current_level, lives):
        self.level = Level(current_level, screen, self.create_overworld, self.create_level, self.create_main_menu, lives)
        self.status = 'level'

    # Creates the overworld
    def create_overworld(self, current_level, new_max_level, lives):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level, self.create_main_menu, lives)
        self.status = 'overworld'

    # Creates the main menu
    def create_main_menu(self, current_level, max_level, lives, reset):
        if reset == 1:
            self.max_level = 0
        self.main_menu = main_menu(current_level, max_level, screen, self.create_overworld, lives)
        self.status = 'main_menu'

    # Decides what state the game is in
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
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT + 1:
                if game.level is not None:
                    game.level.updatetimer()

        game.run()

        pygame.display.update()
        clock.tick(60)