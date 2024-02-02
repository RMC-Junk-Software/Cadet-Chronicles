import pygame
from tiles import Tile, StaticTile
from settings import tile_x, tile_y, screen_width, screen_height, speed, jump_speed
from player import Player
from support import import_csv_layout, import_cut_graphics


class Level:
    def __init__(self, level_data, skin, surface):
        self.display_surface = surface
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.skin = skin

        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_x
                    y = row_index * tile_y

                    if type == 'terrain':
                        tile_surface = pygame.image.load('../Graphics/Textures/tile.png').convert()
                        sprite = StaticTile(tile_x, tile_y, x, y, tile_surface)
                        sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_x
                y = row_index * tile_y
                if val == '0':
                    sprite = Player(self.skin, (x,y))
                    self.player.add(sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/3 and direction_x < 0:
            self.world_shift_x = speed
            player.speed = 0

        elif player_x > (screen_width - screen_width/3) and direction_x > 0:
            self.world_shift_x = -speed
            player.speed = 0

        else:
            self.world_shift_x = 0
            player.speed = speed

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_y < screen_height/5 and direction_y < 0:
            self.world_shift_y = 20
            direction_y = 0

        elif player_y > (screen_height - screen_height/5) and direction_y > 0:
            self.world_shift_y = -20
            direction_y = 0

        else:
            player.jump_speed = jump_speed
            self.world_shift_y = 0


    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.can_jump = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self):

        self.terrain_sprites.update(self.world_shift_x, self.world_shift_y)
        self.terrain_sprites.draw(self.display_surface)

        self.horizontal_movement_collision()
        self.vertical_movement_collision()

        self.scroll_x()
        self.scroll_y()

        self.player.update()
        self.player.draw(self.display_surface)

        self.goal.update(self.world_shift_x)
        self.goal.draw(self.display_surface)

