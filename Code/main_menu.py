import pygame


class Node(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((200, 80))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)


class main_menu:
    def __init__(self, current_level, max_level, surface, create_overworld):
        self.current_level = current_level
        self.max_level = max_level
        self.display_surface = surface
        self.create_overworld = create_overworld

        self.setup_nodes()
        self.mouse = pygame.Rect(0, 0, 5, 5)

    def setup_nodes(self):
        self.node1 = pygame.sprite.GroupSingle()
        self.node2 = pygame.sprite.GroupSingle()

        play_button = Node((500, 400))
        self.node1.add(play_button)

        back_button = Node((500, 500))
        self.node2.add(back_button)

    def check_mouse(self):
        self.mouse.center = pygame.mouse.get_pos()

        if self.node1.sprite.rect.colliderect(self.mouse):
            self.node1.sprite.image.fill('green')
            if pygame.mouse.get_pressed()[0]:
                self.create_overworld(self.current_level, self.max_level)
        else:
            self.node1.sprite.image.fill('red')

        if self.node2.sprite.rect.colliderect(self.mouse):
            self.node2.sprite.image.fill('green')
            if pygame.mouse.get_pressed()[0]:
                self.create_overworld(self.current_level, self.max_level)
        else:
            self.node2.sprite.image.fill('red')

    def run(self):
        self.node1.draw(self.display_surface)
        self.node2.draw(self.display_surface)
        self.check_mouse()
