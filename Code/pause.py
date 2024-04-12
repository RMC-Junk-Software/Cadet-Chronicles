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
        self.title_pos = (500, 50)
        self.button1 = ''
        self.button1_pos = (0,0)
        self.button2 = ''
        self.button2_pos = (0,0)
        if self.status == 'pause':
            self.title = 'Paused'
            self.button1 = 'Continue'
            self.button1_pos = (350, 340)
            self.button2 = 'Levels'
            self.button2_pos = (650, 340)
        elif self.status == 'LOP':
            self.title = 'You Failed'
            self.button1 = 'LOP'
            self.button1_pos = (350, 560)
            self.button2 = 'Quit'
            self.button2_pos = (650, 560)
        elif self.status == 'winner':
            self.title = 'You Graduated!'
            self.title_pos = (500, 300)
            self.button1 = 'Main Menu'
            self.button1_pos = (500, 350)
            self.button2 = 'High Scores'
            self.button2_pos = (500, 450)
        elif self.status == 'dead':
            self.title = 'You Failed Out'
            self.button1 = 'Main Menu'
            self.button1_pos = (500, 250)
        elif self.status == 'scores':
            self.title = 'High Scores'
            self.button1 = 'Back'
            self.button1_pos = (100, 50)
            self.level1 = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("Level 1: {score} seconds".format(score=self.current_level), True, (255, 255, 255))
            self.level1_rect = self.level1.get_rect(topleft=(350, 200))
            self.level2 = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("Level 2: {score} seconds".format(score=self.max_level), True, (255, 255, 255))
            self.level2_rect = self.level2.get_rect(topleft=(350, 300))
            self.level3 = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("Level 3: {score} seconds".format(score=self.lives), True, (255, 255, 255))
            self.level3_rect = self.level3.get_rect(topleft=(350, 400))
            self.level4 = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("Level 4: {score} seconds".format(score=self.create_overworld), True, (255, 255, 255))
            self.level4_rect = self.level4.get_rect(topleft=(350, 500))

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

            self.run()

            pygame.display.update()
            self.clock.tick(60)

    def pause_screen(self):
        self.play = pygame.sprite.GroupSingle()
        self.back = pygame.sprite.GroupSingle()

        self.title_text = pygame.font.Font("./fonts/EDITIA__.TTF", 50).render(self.title, True, (255, 255, 255))
        self.title_text_rect = self.title_text.get_rect(center=(500, 50))

        play_button = Node(self.button1_pos)
        self.play.add(play_button)
        self.Start_Text = pygame.font.Font("./fonts/EDITIA__.TTF", 25).render(self.button1, True, (255,255,255))
        self.start_text_rect = self.Start_Text.get_rect(center=play_button.rect.center)

        back_button = Node(self.button2_pos)
        self.back.add(back_button)
        self.Exit_text = pygame.font.Font("./fonts/EDITIA__.TTF", 25).render(self.button2, True, (255, 255, 255))
        self.exit_text_rect = self.Exit_text.get_rect(center=back_button.rect.center)

    def check_mouse(self):
        self.mouse.center = pygame.mouse.get_pos()

        if self.play.sprite.rect.colliderect(self.mouse):
            self.play.sprite.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                if self.status == 'pause':
                    self.loop = 0
                elif self.status == 'LOP':
                    self.create_overworld(self.current_level, 0, self.lives, 500)
                    self.loop = 0
                elif self.status == 'winner':
                    self.create_main_menu(0, 0, 2, 1)
                    self.loop = 0
                elif self.status == 'dead':
                    self.create_main_menu(0, 0, 2, 1)
                    self.loop = 0
                elif self.status == 'scores':
                    self.loop = 0
        else:
            self.play.sprite.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()

        if self.back.sprite.rect.colliderect(self.mouse):
            self.back.sprite.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                if self.status == 'pause':
                    self.create_overworld(self.current_level, 0, self.lives, 500)
                    self.loop = 0
                elif self.status == 'LOP':
                    self.create_main_menu(0, 0, 2, 1)
                    self.loop = 0
                elif self.status == 'winner':
                    Pause(self.current_level, self.max_level, self.display_surface, self.lives, self.create_overworld, self.create_main_menu, 'scores')
                elif self.status == 'dead':
                    pass
                elif self.status == 'scores':
                    pass
        else:
            self.back.sprite.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()

    def run(self):

        if self.status == 'pause':
            bg = pygame.image.load('../Graphics/Textures/Backgrounds/Pause_bg.png').convert()
        elif self.status == 'LOP':
            bg = pygame.image.load('../Graphics/Textures/Backgrounds/LOP_bg.png').convert()
        elif self.status == 'winner':
            bg = pygame.image.load('../Graphics/Textures/Backgrounds/Winner_bg.png').convert()
        elif self.status == 'dead':
            bg = pygame.image.load('../Graphics/Textures/Backgrounds/dead_bg.png').convert()
        elif self.status == 'scores':
            bg = pygame.image.load('../Graphics/Textures/Backgrounds/Scores_bg.png').convert()
        self.display_surface.blit(bg, (0, 0))

        self.play.draw(self.display_surface)
        if self.status == 'pause' or self.status == 'LOP' or self.status == 'winner':
            self.back.draw(self.display_surface)
            self.display_surface.blit(self.Exit_text, self.exit_text_rect)
        if self.status == 'scores':
            self.display_surface.blit(self.level1, self.level1_rect)
            self.display_surface.blit(self.level2, self.level2_rect)
            self.display_surface.blit(self.level3, self.level3_rect)
            self.display_surface.blit(self.level4, self.level4_rect)
        self.display_surface.blit(self.Start_Text, self.start_text_rect)
        self.display_surface.blit(self.title_text, self.title_text_rect)

        self.check_mouse()
