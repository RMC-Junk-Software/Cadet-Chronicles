import pygame
from tiles import Tile
from settings import tile_x, tile_y, screen_width, speed
from player import Player

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0


    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_in, row in enumerate(layout):
            for col_in, item in enumerate(row):
                if item == 'X':
                    x = col_in * tile_x
                    y = row_in * tile_y
                    tile = Tile((x,y), (tile_x, tile_y))
                    self.tiles.add(tile)

                if item == 'P':
                    x = col_in * tile_x
                    y = row_in * tile_y
                    player = Player((x,y))
                    self.player.add(player)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/5 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0

        elif player_x > (screen_width - screen_width/5) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0

        else:
            self.world_shift = 0
            player.speed = speed

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.can_jump = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0


    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()


        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
