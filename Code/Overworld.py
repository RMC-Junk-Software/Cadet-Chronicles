import pygame
from Game_data import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == 'available':
            self.image.fill('red')
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(center = pos)


class Overworld:
    def __init__(self, current_level, max_level, surface, create_level, create_main_menu):

        self.current_level = current_level
        self.max_level = max_level
        self.display_surface = surface

        self.create_level = create_level
        self.create_main_menu = create_main_menu
        self.mouse = pygame.Rect(0, 0, 5, 5)

        self.setup_nodes()
        self.back_button()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available')
            else:
                node_sprite = Node(node_data['node_pos'], 'locked')
            self.nodes.add(node_sprite)

    def back_button(self):
        self.back = pygame.sprite.GroupSingle()
        node_sprite = Node((60,50), 'available')
        self.back.add(node_sprite)

    def draw_paths(self):
        if self.max_level > 0:
            points1 = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, 'green', False, points1, 6)
        if self.max_level < 3:
            points2 = [node['node_pos'] for index, node in enumerate(levels.values()) if index >= self.max_level]
            pygame.draw.lines(self.display_surface, 'red', False, points2, 6)

    def check_mouse(self):
        self.mouse.center = pygame.mouse.get_pos()
        for index, sprites in enumerate(self.nodes.sprites()):
            if sprites.rect.colliderect(self.mouse):
                if index <= self.max_level:
                    sprites.image.fill('green')
                    if pygame.mouse.get_pressed()[0]:
                        self.create_level(levels[index])
            else:
                if index <= self.max_level:
                    sprites.image.fill('red')

        if self.back.sprite.rect.colliderect(self.mouse):
            self.back.sprite.image.fill('green')
            if pygame.mouse.get_pressed()[0]:
                self.create_main_menu(self.current_level, self.max_level)
        else:
            self.back.sprite.image.fill('red')

    def run(self):
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.back.draw(self.display_surface)
        self.check_mouse()
