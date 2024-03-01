import pygame
from tiles import Tile, StaticTile, Collectibles
from settings import tile_x, tile_y, screen_width, screen_height, speed, jump_speed
from player import Player
from support import import_csv_layout, import_cut_graphics
import Camera


class Level:
    def __init__(self, level_data, surface, create_overworld, create_level):
        self.current_level = level_data
        self.new_max_level = level_data['unlock']
        self.display_surface = surface
        self.create_overworld = create_overworld
        self.create_level = create_level

        self.world_shift_x = 0
        self.world_shift_y = 0

        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        self.camera = None

        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        collectible_layout = import_csv_layout(level_data['collectible'])
        self.collectible_sprites = self.create_tile_group(collectible_layout, 'collectible')

    def input(self):
        keys = pygame.key.get_pressed()
        player = self.player.sprite

        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level, 0)
        elif pygame.sprite.spritecollide(player, self.goal, False):
            if self.new_max_level == 4:
                # game complete code
                print("Game complete!")
            self.create_overworld(self.current_level, self.new_max_level)
        # death code
        # elif player.rect.centery < -30:
        #     self.create_level(self.current_level)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_x
                    y = row_index * tile_y

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(self.current_level['terrain_skin'])
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_x, tile_y, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == 'collectible':
                        sprite = Collectibles(tile_x, tile_y, x, y, self.current_level['collectible_skin'])
                        sprite_group.add(sprite)

        x = (col_index+1)*tile_x
        y = (row_index + 1) * tile_y

        self.camera = Camera.Camera(Camera.complex_camera, x, y)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_x
                y = row_index * tile_y
                if val == '0':
                    sprite = Player(self.current_level['player_skin'], (x,y))
                    self.player.add(sprite)
                if val == '1':
                    end_tile = pygame.image.load('../Graphics/Character/elof.png')
                    sprite = StaticTile(tile_x, tile_y, x, y, end_tile)
                    self.goal.add(sprite)


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

    def collectible_collision(self):
        collided = pygame.sprite.spritecollide(self.player.sprite, self.collectible_sprites, True)

    def run(self):

        self.input()

        self.camera.update(self.player.sprite)

        self.terrain_sprites.update(self.world_shift_x, self.world_shift_y)
        for tile in self.terrain_sprites:
            self.display_surface.blit(tile.image, self.camera.apply(tile))

        self.collectible_sprites.update(self.world_shift_x, self.world_shift_y)
        for tile in self.collectible_sprites:
            self.display_surface.blit(tile.image, self.camera.apply(tile))
        self.collectible_collision()

        self.horizontal_movement_collision()
        self.vertical_movement_collision()

        self.player.update()
        self.display_surface.blit(self.player.sprite.image, self.camera.apply(self.player.sprite))

        self.goal.update(self.world_shift_x, self.world_shift_y)
        self.display_surface.blit(self.goal.sprite.image, self.camera.apply(self.goal.sprite))

