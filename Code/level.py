import pygame
from tiles import StaticTile, Tile
from settings import tile_x, tile_y
from player import Player
from support import import_csv_layout, import_cut_graphics, textOutline
from pause import Pause
from enemies import Enemy
import Camera

White = (255, 255, 255)
Black = (10,10,10)

class Level:
    def __init__(self, level_data, surface, create_overworld, create_level, create_main_menu, lives):
        self.current_level = level_data
        self.new_max_level = level_data['unlock']
        self.display_surface = surface
        self.create_overworld = create_overworld
        self.create_level = create_level
        self.create_main_menu = create_main_menu
        self.lives = lives

        # Sounds

        self.collect_sound = pygame.mixer.Sound("../Sounds/Collect.mp3")
        self.last_collect_sound = pygame.mixer.Sound("../Sounds/Final_Collect.mp3")
        self.hurt_sound = pygame.mixer.Sound("../Sounds/Injure.wav")
        self.death_sound = pygame.mixer.Sound("../Sounds/Death.mp3")

        pygame.mixer.music.set_volume(.2)
        pygame.mixer.music.load(level_data['music'])
        pygame.mixer.music.play(-1)

        self.camera = None
        self.font = pygame.font.Font("./fonts/EDITIA__.TTF", 25)

        # Collectibles text
        self.collected = 0
        self.collectible_text = textOutline(self.font, "Collectibles: {collect}/9".format(collect=self.collected), White, Black)
        self.collectible_text_rect = pygame.Surface((300,30)).get_rect(topleft=(5,40))

        # Health text
        self.health = 3
        self.health_text = textOutline(self.font, "Health: {health}".format(health=self.health), White, Black)
        self.invincible = 0
        self.hit = 0
        self.hurt_time = 0
        self.hurt_time2 = 0
        self.health_text_rect = pygame.Surface((300, 30)).get_rect(topleft=(5, 8))

        #timer text
        self.timer = 0
        self.timer_text = textOutline(self.font, "Time: {time}".format(time=self.timer),
                                            White, Black)
        self.timer_text_rect = pygame.Surface((300, 30)).get_rect(topleft=(5, 70))

        # Player sprite
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Terrain sprites
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # Indoor sprites
        indoor_layout = import_csv_layout(level_data['indoor'])
        self.indoor_sprites = self.create_tile_group(indoor_layout, 'indoor')

        # Collectibles sprites
        collectible_layout = import_csv_layout(level_data['collectible'])
        self.collectible_sprites = self.create_tile_group(collectible_layout, 'collectible')

        # Obstacle sprites
        obstacle_layout = import_csv_layout(level_data['obstacle'])
        self.obstacle_sprites = self.create_tile_group(obstacle_layout, 'obstacle')

        # Enemy sprites
        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')

        # Constraints sprites
        constraint_layout = import_csv_layout(level_data['constraint'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

        # Flag sprites
        flag_layout = import_csv_layout(level_data['flag'])
        self.flag_lowered = self.create_tile_group(flag_layout, 'flag_lowered')
        self.flag_raised = self.create_tile_group(flag_layout, 'flag_raised')

        # Background
        self.bg = pygame.image.load(level_data['background']).convert()

    # Check various inputs
    def input(self):
        keys = pygame.key.get_pressed()
        player = self.player.sprite

        if keys[pygame.K_ESCAPE]:
            Pause(self.current_level, self.new_max_level, self.display_surface, self.lives, self.create_overworld, self.create_main_menu, 'pause')
        if pygame.sprite.spritecollide(player, self.flag_raised, False):
            if self.collected >= 9:
                if self.new_max_level == 4:
                    Pause(self.current_level, self.new_max_level, self.display_surface, self.lives,
                          self.create_overworld, self.create_main_menu, 'winner')
                else:
                    self.create_overworld(self.current_level, self.new_max_level, self.lives)
        if self.health <= 0 and self.lives == 2:
            self.death_sound.play()
            Pause(self.current_level, self.new_max_level, self.display_surface, self.lives - 1, self.create_overworld,
                  self.create_main_menu, 'LOP')
        if self.health <= 0 and self.lives == 1:
            Pause(self.current_level, self.new_max_level, self.display_surface, self.lives - 1, self.create_overworld,
                  self.create_main_menu, 'dead')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        if type == 'terrain':
            terrain_tile_list = import_cut_graphics(self.current_level['terrain_skin'])
        if type == 'indoor':
            indoor_tile_list = import_cut_graphics(self.current_level['indoor_skin'])

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_x
                    y = row_index * tile_y

                    if type == 'terrain':
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_x, tile_y, x, y, tile_surface)

                    if type == 'indoor':
                        tile_surface = indoor_tile_list[int(val)]
                        sprite = StaticTile(tile_x, tile_y, x, y, tile_surface)

                    if type == 'collectible':
                        terrain_tile_list = import_cut_graphics('../Graphics/Sprites/Level1-4CollectiblesV2.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_x, tile_y, x, y, tile_surface)

                    if type == 'obstacle':
                        terrain_tile_list = import_cut_graphics(self.current_level['obstacle_skin'])
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_x, tile_y, x, y, tile_surface)

                    if type == 'enemy':
                        skin = pygame.image.load(self.current_level['enemy_skin'])
                        sprite = Enemy(tile_x, tile_y, x, y, skin)

                    if type == 'constraint':
                        sprite = Tile(tile_x, tile_y, x, y)

                    if type == 'flag_lowered':
                        flag_tile_list = import_cut_graphics('../Graphics/Sprites/FlagLowered.png')
                        tile_surface = flag_tile_list[int(val)]
                        sprite = StaticTile(tile_x, tile_y, x, y, tile_surface)

                    if type == 'flag_raised':
                        flag_tile_list = import_cut_graphics('../Graphics/Sprites/FlagRaised.png')
                        tile_surface = flag_tile_list[int(val)]
                        sprite = StaticTile(tile_x, tile_y, x, y, tile_surface)

                    sprite_group.add(sprite)

        x = (col_index + 1) * tile_x
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
        if collided:
            if self.collected < 8:
                self.collect_sound.play()
            else:
                self.last_collect_sound.play()
            self.collected += 1
            self.collectible_text = textOutline(self.font, "Colletibles: {collect}/9".format(collect=self.collected), White, Black)
            self.collectible_text_rect = pygame.Surface((300, 30)).get_rect(topleft=(5, 40))

    def damage_collision(self, x_sprites):
        player = self.player.sprite

        current_time = pygame.time.get_ticks()

        if current_time - self.hurt_time >= 40 and self.hit == 1:
            self.invincible = 0
            if current_time - self.hurt_time >= 60:
                self.hit = 0
        if current_time - self.hurt_time2 >= 800 and self.hit == 0:
            self.invincible = 0

        for sprite in x_sprites.sprites():
            if sprite.rect.colliderect(player.rect) and self.invincible == 0:
                if self.hit == 1:
                    self.hurt_sound.play()
                    self.health += -1
                    self.health_text = textOutline(self.font, "Health: {health}".format(health=self.health), White,
                                                   Black)
                    self.invincible = 1
                    self.hit = 0
                    self.hurt_time2 = pygame.time.get_ticks()
                else:
                    self.invincible = 1
                    self.hit = 1
                    self.hurt_time = pygame.time.get_ticks()

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def updatetimer(self):
        self.timer += 1
        self.timer_text = textOutline(self.font, "Time: {time}".format(time=self.timer),
                                      White, Black)
        self.timer_text_rect = pygame.Surface((300, 30)).get_rect(topleft=(5, 70))

    def run(self):

        self.display_surface.blit(self.bg, (0, 0))

        self.input()

        self.camera.update(self.player.sprite)

        # Update tiles
        for tile in self.terrain_sprites:
            self.display_surface.blit(tile.image, self.camera.apply(tile))

        for tile in self.indoor_sprites:
            self.display_surface.blit(tile.image, self.camera.apply(tile))

        for tile in self.collectible_sprites:
            self.display_surface.blit(tile.image, self.camera.apply(tile))

        for tile in self.obstacle_sprites:
            self.display_surface.blit(tile.image, self.camera.apply(tile))

        for tile in self.enemy_sprites:
            self.display_surface.blit(tile.image, self.camera.apply(tile))

        # Collisions
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.collectible_collision()
        self.damage_collision(self.obstacle_sprites)
        self.damage_collision(self.enemy_sprites)

        # Enemies
        self.enemy_sprites.update()
        self.enemy_collision_reverse()

        # Flag lowered or raised
        if self.collected < 9:
            for tile in self.flag_lowered:
                self.display_surface.blit(tile.image, self.camera.apply(tile))
        else:
            for tile in self.flag_raised:
                self.display_surface.blit(tile.image, self.camera.apply(tile))

        # Update player
        self.player.update()
        self.display_surface.blit(self.player.sprite.image, self.camera.apply(self.player.sprite))

        # Display HUD
        self.display_surface.blit(self.collectible_text, self.collectible_text_rect)
        self.display_surface.blit(self.health_text, self.health_text_rect)
        self.display_surface.blit(self.timer_text, self.timer_text_rect)
