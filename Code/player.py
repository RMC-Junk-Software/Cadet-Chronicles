import pygame.sprite
from settings import speed, gravity, jump_speed

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((60,120))
        self.image.fill('Red')
        self.rect = self.image.get_rect(midleft = pos)
        self.direction = pygame.math.Vector2(0,0)

        # Movement
        self.speed = speed
        self.gravity = gravity
        self.jump_speed = jump_speed

    def get_input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump()


    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
    def update(self):
        self.get_input()