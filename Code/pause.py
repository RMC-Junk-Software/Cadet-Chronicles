import pygame, sys
from settings import *


# Allows us to create nodes that act as buttons
class Node(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((200, 80))
        self.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)


class Pause:
    def __init__(self, current_level, max_level, surface, lives, create_overworld, create_main_menu, status):
        self.current_level = current_level
        self.max_level = max_level
        self.display_surface = surface
        self.lives = lives
        self.create_overworld = create_overworld
        self.create_main_menu = create_main_menu
        self.status = status

        self.title = ''
        self.button1 = ''
        self.button2 = ''
        if self.status == 'pause':
            self.title = 'Paused'
            self.button1 = 'Continue'
            self.button2 = 'Levels'
        elif self.status == 'LOP':
            self.title = 'You Failed'
            self.button1 = 'LOP'
            self.button2 = 'Quit'
        elif self.status == 'winner':
            self.title = 'You Graduated!'
            self.button1 = 'Main Menu'
        elif self.status == 'dead':
            self.title = 'You Failed Out'
            self.button1 = 'Main Menu'

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.pause_screen()
        self.mouse = pygame.Rect(0, 0, 5, 5)

        self.loop = 1
        while self.loop == 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            bg = pygame.image.load('../Graphics/Textures/bg.png').convert()
            self.screen.blit(bg, (0, 0))

            self.run()

            pygame.display.update()
            self.clock.tick(60)

    def pause_screen(self):
        self.play = pygame.sprite.GroupSingle()
        self.back = pygame.sprite.GroupSingle()

        self.title_text = pygame.font.Font("./fonts/EDITIA__.TTF", 40).render(self.title, True, (255, 255, 255))
        self.title_text_rect = self.title_text.get_rect(center=(500, 50))

        play_button = Node((300, 350))
        self.play.add(play_button)
        self.Start_Text = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render(self.button1, True, (255,255,255))
        self.start_text_rect = self.Start_Text.get_rect(center=play_button.rect.center)

        back_button = Node((700, 350))
        self.back.add(back_button)
        self.Exit_text = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render(self.button2, True, (255, 255, 255))
        self.exit_text_rect = self.Exit_text.get_rect(center=back_button.rect.center)

    def check_mouse(self):
        self.mouse.center = pygame.mouse.get_pos()

        if self.play.sprite.rect.colliderect(self.mouse):
            self.play.sprite.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                if self.status == 'pause':
                    self.loop = 0
                elif self.status == 'LOP':
                    self.create_overworld(self.current_level, 0, self.lives)
                    self.loop = 0
                elif self.status == 'winner':
                    self.create_main_menu(0, 0, 2, 1)
                    self.loop = 0
                elif self.status == 'dead':
                    self.create_main_menu(0, 0, 2, 1)
                    self.loop = 0
        else:
            self.play.sprite.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()

        if self.back.sprite.rect.colliderect(self.mouse):
            self.back.sprite.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                if self.status == 'pause':
                    self.create_overworld(self.current_level, 0, self.lives)
                    self.loop = 0
                elif self.status == 'LOP':
                    self.create_main_menu(0, 0, 2, 1)
                    self.loop = 0
                elif self.status == 'winner':
                    pass
                elif self.status == 'dead':
                    pass
        else:
            self.back.sprite.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()

    def run(self):

        self.play.draw(self.display_surface)
        self.back.draw(self.display_surface)
        self.display_surface.blit(self.Start_Text, self.start_text_rect)
        self.display_surface.blit(self.Exit_text, self.exit_text_rect)
        self.display_surface.blit(self.title_text, self.title_text_rect)

        self.check_mouse()
