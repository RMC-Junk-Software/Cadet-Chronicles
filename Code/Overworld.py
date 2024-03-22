import pygame
from Game_data import levels


# Allows us to create nodes that act as buttons for each level
class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status):
        super().__init__()

        if status == 'available':
            self.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()
        else:
            self.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class Overworld:
    def __init__(self, current_level, max_level, surface, create_level, create_main_menu, lives):

        self.current_level = current_level
        self.max_level = max_level
        self.display_surface = surface
        self.lives = lives

        self.text = [pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("1st Year", True, (255, 255, 255)),pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("2nd Year", True, (255, 255, 255)),pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("3rd Year", True, (255, 255, 255)),pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("4th Year", True, (255, 255, 255)),pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("Back", True, (255, 255, 255)),pygame.font.Font("./fonts/EDITIA__.TTF", 30).render("lives: {lives}/2".format(lives=self.lives), True, (255, 255, 255))]
        self.text_rect = []

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
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available')
            else:
                node_sprite = Node(node_data['node_pos'], 'locked')
            self.nodes.add(node_sprite)

            self.text_rect.append(self.text[index].get_rect(center=node_sprite.rect.center))

    # Setup back button
    def back_button(self):
        self.back = pygame.sprite.GroupSingle()
        node_sprite = Node((100,50), 'available')
        self.back.add(node_sprite)
        self.text_rect.append(self.text[4].get_rect(center=node_sprite.rect.center))

    # Setup lives text
    def lives_text(self):
        self.life = pygame.sprite.GroupSingle()
        node_sprite = Node((500, 50), 'locked')
        self.life.add(node_sprite)
        self.text_rect.append(self.text[5].get_rect(center=node_sprite.rect.center))

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
            if sprites.rect.colliderect(self.mouse):
                if index <= self.max_level:
                    sprites.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
                    if pygame.mouse.get_pressed()[0]:
                        self.create_level(levels[index], self.lives)
            else:
                if index > self.max_level:
                    sprites.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
                else:
                    sprites.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()

        if self.back.sprite.rect.colliderect(self.mouse):
            self.back.sprite.image = pygame.image.load("../UI/SelectedButtonBubble.png").convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                self.create_main_menu(self.current_level, self.max_level, self.lives, 0)
        else:
            self.back.sprite.image = pygame.image.load("../UI/UnselectedButtonBubble.png").convert_alpha()

    def run(self):
        self.draw_paths()
        self.nodes.draw(self.display_surface)

        self.back.draw(self.display_surface)
        self.life.draw(self.display_surface)
        for i in range(len(self.text)):
            self.display_surface.blit(self.text[i], self.text_rect[i])

        current_time = pygame.time.get_ticks()
        time = current_time - self.time
        if time > 300:
            self.check_mouse()
