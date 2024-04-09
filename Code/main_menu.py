import sys
import pygame
from support import textOutline


# Allows us to create nodes that act as buttons
class Node(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((200, 80))
        self.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)


class main_menu:
    def __init__(self, current_level, max_level, surface, create_overworld, lives):
        self.current_level = current_level
        self.max_level = max_level
        self.display_surface = surface
        self.create_overworld = create_overworld
        self.lives = lives

        self.setup_nodes()
        self.mouse = pygame.Rect(0, 0, 5, 5)
        self.time = pygame.time.get_ticks()


    # Setup play and quit buttons
    def setup_nodes(self):
        self.play = pygame.sprite.GroupSingle()
        self.quit = pygame.sprite.GroupSingle()
        self.instructions = pygame.sprite.GroupSingle()

        self.title_text = pygame.font.Font("./fonts/EDITIA__.TTF", 40).render("Cadet Chronicles: March to the Arch", True, (255, 255, 255))
        self.title_text_rect = self.title_text.get_rect(center=(500, 50))

        play_button = Node((500, 150))
        self.play.add(play_button)
        self.Start_Text = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("Start", True, (255,255,255))
        self.start_text_rect = self.Start_Text.get_rect(center=play_button.rect.center)

        back_button = Node((800, 150))
        self.quit.add(back_button)
        self.Exit_text = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("Exit", True, (255, 255, 255))
        self.exit_text_rect = self.Exit_text.get_rect(center=back_button.rect.center)

        instruction_button = Node((200, 150))
        self.instructions.add(instruction_button)
        self.Instruction_text = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("Help", True,(255, 255, 255))
        self.Instruction_text_rect = self.Instruction_text.get_rect(center=instruction_button.rect.center)

    # Check if mouse is above any buttons
    def check_mouse(self):
        self.mouse.center = pygame.mouse.get_pos()

        if self.play.sprite.rect.colliderect(self.mouse):
            self.play.sprite.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                self.create_overworld(self.current_level, self.max_level, self.lives)
        else:
            self.play.sprite.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()

        if self.quit.sprite.rect.colliderect(self.mouse):
            self.quit.sprite.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()
        else:
            self.quit.sprite.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()

        if self.instructions.sprite.rect.colliderect(self.mouse):
            self.instructions.sprite.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()

            # create an instruction window that is shown by hovering over it
            instruction_window = pygame.image.load("../Graphics/Textures/CChowtoplay.png")
            self.display_surface.blit(instruction_window, (0, 0))

        else:
            self.instructions.sprite.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()

    def run(self):

        bg = pygame.image.load('../UI/HomeScreenScaled.png').convert()
        self.display_surface.blit(bg, (0, 0))
        self.play.draw(self.display_surface)
        self.quit.draw(self.display_surface)
        self.instructions.draw(self.display_surface)
        self.display_surface.blit(self.Start_Text, self.start_text_rect)
        self.display_surface.blit(self.Exit_text, self.exit_text_rect)
        self.display_surface.blit(self.Instruction_text, self.Instruction_text_rect)
        self.display_surface.blit(self.title_text, self.title_text_rect)

        current_time = pygame.time.get_ticks()
        time = current_time - self.time
        if time > 300:
            self.check_mouse()
        self.check_mouse()
