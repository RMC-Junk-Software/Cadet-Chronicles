import pygame
from Game_data import levels


# Allows us to create nodes that act as buttons for each level
class Node_levels(pygame.sprite.Sprite):
    def __init__(self, pos, status, current_level):
        super().__init__()

        if status == 'available':
            self.image = pygame.image.load(current_level['unselected_button']).convert_alpha()
        else:
            self.image = pygame.image.load(current_level['selected_button']).convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status):
        super().__init__()

        if status == 'available':
            self.image = pygame.image.load('../UI/UnselectedButtonBubble.png').convert_alpha()
        else:
            self.image = pygame.image.load('../UI/SelectedButtonBubble.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class Overworld:
    def __init__(self, current_level, max_level, surface, create_level, create_main_menu, lives):

        self.current_level = current_level
        self.max_level = max_level
        self.display_surface = surface
        self.lives = lives

        self.create_level = create_level
        self.create_main_menu = create_main_menu
        self.mouse = pygame.Rect(0, 0, 5, 5)

        self.setup_nodes()
        self.back_button()
        self.lives_text()
        self.time = pygame.time.get_ticks()

    # Setup buttons for each level
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            current_level = levels[index]
            if index <= self.max_level:
                node_sprite = Node_levels(node_data['node_pos'], 'available', current_level)
            else:
                node_sprite = Node_levels(node_data['node_pos'], 'locked', current_level)
            self.nodes.add(node_sprite)

    # Setup back button
    def back_button(self):
        self.back = pygame.sprite.GroupSingle()
        self.back_text = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("Back", True, (255, 255, 255))
        node_sprite = Node((100,50), 'available')
        self.back.add(node_sprite)
        self.back_text_rect = self.back_text.get_rect(center=node_sprite.rect.center)

    # Setup lives text
    def lives_text(self):
        self.life = pygame.sprite.GroupSingle()
        self.life_text = pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("lives: {lives}/2".format(lives=self.lives), True, (255, 255, 255))
        node_sprite = Node((500, 50), 'locked')
        self.life.add(node_sprite)
        self.life_text_rect = self.life_text.get_rect(center=node_sprite.rect.center)

    # Create green and red paths between levels
    def draw_paths(self):
        if self.max_level > 0:
            points1 = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, 'green', False, points1, 6)
        if self.max_level < 3:
            points2 = [node['node_pos'] for index, node in enumerate(levels.values()) if index >= self.max_level]
            pygame.draw.lines(self.display_surface, 'red', False, points2, 6)

    # Check for mouse inputs
    def check_mouse(self):
        self.mouse.center = pygame.mouse.get_pos()
        for index, sprites in enumerate(self.nodes.sprites()):
            current_level = levels[index]
            if sprites.rect.colliderect(self.mouse):
                if index <= self.max_level:
                    sprites.image = pygame.image.load(current_level['selected_button']).convert_alpha()
                    if pygame.mouse.get_pressed()[0]:
                        self.create_level(levels[index], self.lives)
            else:
                if index > self.max_level:
                    sprites.image = pygame.image.load(current_level['selected_button']).convert_alpha()
                else:
                    sprites.image = pygame.image.load(current_level['unselected_button']).convert_alpha()

        if self.back.sprite.rect.colliderect(self.mouse):
            self.back.sprite.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                self.create_main_menu(self.current_level, self.max_level, self.lives, 0)
        else:
            self.back.sprite.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()

    def run(self):

        bg = pygame.image.load('../Graphics/Textures/Backgrounds/Levels_bg.png').convert()
        self.display_surface.blit(bg, (0, 0))

        self.draw_paths()
        self.nodes.draw(self.display_surface)

        self.back.draw(self.display_surface)
        self.life.draw(self.display_surface)
        self.display_surface.blit(self.back_text, self.back_text_rect)
        self.display_surface.blit(self.life_text, self.life_text_rect)

        current_time = pygame.time.get_ticks()
        time = current_time - self.time
        if time > 300:
            self.check_mouse()
