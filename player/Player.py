# this file contain Player class

import sys
sys.path.append('../')
from core.config import *
import pygame
from pygame.math import Vector2
from pygame.locals import *
from numpy import sign


class Animation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.n_animations = 0
        self.current_running_sprite = 0

    def load_player_body(self, player_images=[], sprite_sheet=False):
        self.sprites = []
        if not sprite_sheet:
            for image_name in player_images:
                try:
                    sprite = pygame.image.load(image_name + ".png").convert()
                    sprite.set_colorkey((255, 255, 255))
                    sprite = pygame.transform.scale(sprite, (TILE_SIZE/4, TILE_SIZE/2))
                    self.sprites.append(sprite)
                    self.n_animations += 1
                except FileNotFoundError as e:
                    print(e) # inform which file does not exist
            if self.sprites:
                self.rect = self.sprites[0].get_rect()
                self.sprites_flipped = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites]
                self.current_running_sprite = 0
                self.image = self.sprites[self.current_running_sprite]
            else:
                self.rect = pygame.Rect(0,0,TILE_SIZE,TILE_SIZE)
                return False

        elif sprite_sheet:
            self.sprites = {}
            self.sprites_flipped = {}
            for type, values in player_images.items():
                self.n_animations = values[1]
                self.sprites[type] = [self.n_animations, []]
                self.sprites_flipped[type] = [self.n_animations, []]
                self.sprite_sheet = pygame.image.load(values[0]).convert()
                self.sprite_width = self.sprite_sheet.get_size()[0] / self.n_animations
                self.sprite_height = self.sprite_sheet.get_size()[1]
                for x in range(self.n_animations):
                    self.sprites[type][1].append(self.get_sprite(x*self.sprite_width,0,self.sprite_width,self.sprite_height))
                    self.sprites_flipped[type][1].append(pygame.transform.flip(self.sprites[type][1][x], True, False))
            self.rect = self.sprites['run'][1][0].get_rect()
            
        return True

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w,h-20))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0,0), (x, y, w, h))
        return sprite

    def right(self, dt, facing_left):
        dt /= 10 # normalize
        self.current_running_sprite += dt
        index = int(self.current_running_sprite%self.sprites['run'][0])
        if not facing_left:
            self.image = self.sprites['run'][1][index]
        else:
            self.image = self.sprites_flipped['run'][1][index]

    def left(self, dt):
        dt /= 10 # normalize
        self.current_running_sprite += dt
        self.image = self.sprites_flipped['run'][1][int(self.current_running_sprite%self.sprites_flipped['run'][0])]

    def jump(self, dt):
        dt /= 10 # normalize
        self.current_running_sprite += dt
        try:
            self.image = self.sprites['jump'][1][int(self.current_running_sprite%self.sprites['jump'][0])]
        except KeyError:
            pass

    def standing(self, facing_left):
        #self.current_running_sprite = 0
        if facing_left:
            self.image = self.sprites_flipped['run'][1][0]
        else:
            self.image = self.sprites['run'][1][0]


class Player():
    def __init__(self, gravity=4, max_jumps=1, starting_position=[WINDOW_WIDTH//2,0], acceleration=[0.2,0], max_velocity=5, player_images=None):
        self.base_acceleration = acceleration
        self.max_velocity = abs(max_velocity)
        self.gravity = gravity
        self.vertical_momentum = 0
        self.max_jumps = max_jumps
        self.jumps = 0 # jumps counter
        self.position = Vector2(starting_position) # player's position
        self.shift = Vector2(0,0)
        self.velocity = Vector2([0,0]) # player's velocity
        self.acceleration = Vector2(self.base_acceleration) # player's acceleration
        self.dt = 0
        self.initialize_animation(player_images)
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.pressing = False

    def initialize_animation(self, player_images):
        self.a = Animation()
        if self.a.load_player_body(player_images, False):
            self.animate = True
        else:
            self.animate = False
        self.rect = self.a.rect
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.a)
        self.facing_left = False

    def collide(self, tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def move_left(self):
        self.moving_left = True

    def move_right(self):
        self.moving_right = True

    def move_up(self):
        self.jump = True

    def move(self, dt):
        dt *= 100 # normalize
        self.dt = dt
        self.shift = Vector2(0, 0)
        if abs(self.velocity.x) <= self.max_velocity: # if boundry of max velocity is not crossed
            if self.acceleration.x == 0: self.acceleration.x = self.base_acceleration[0] # if acceleration is turned off then turn it on
            if self.moving_right:
                self.facing_left = False
                self.velocity.x += self.acceleration.x * dt
            if self.moving_left:
                self.facing_left = True
                self.velocity.x -= self.acceleration.x * dt
            if self.moving_left and self.moving_right or not self.moving_left and not self.moving_right:
                if abs(self.velocity.x) < abs(self.acceleration.x): self.velocity.x = 0
                else:
                    self.velocity.x += -sign(self.velocity.x) * self.acceleration.x/10
        else:
            self.acceleration.x = 0
            self.velocity.x = sign(self.velocity.x) * self.max_velocity
        self.shift.x += self.velocity.x * dt
        self.position.x += self.shift.x
        if self.jump:
            if self.jumps < self.max_jumps and not self.pressing:
                self.gravity = 8
                self.vertical_momentum = -self.gravity#-4 # static jump for now
                self.jumps += 1
                self.pressing = True # initialize space pressing
        else:
            self.pressing = False # user stopped pressing space
        self.vertical_momentum += self.gravity/100
        if self.vertical_momentum > self.gravity:
            self.vertical_momentum = self.gravity
        self.shift.y += self.vertical_momentum * dt
        self.position.y += self.shift.y

    def check_collisions(self, dt, tiles):
        collisions = self.collide(tiles)
        for tile in collisions:
            self.acceleration.x = 0
            if self.moving_right:
                self.position.x = tile.rect.x - TILE_SIZE
                self.rect.x = self.position.x
            elif self.moving_left:
                self.position.x = tile.rect.x + TILE_SIZE
                self.rect.x = self.position.x
        self.rect.y = self.position.y
        collisions = self.collide(tiles)
        for tile in collisions:
            if self.vertical_momentum < 0:
                self.position.y += (self.position.y % TILE_SIZE)
                self.rect.y = self.position.y
                self.vertical_momentum = self.gravity/10
            else:
                self.position.y -= (self.position.y % TILE_SIZE)
                self.rect.y = self.position.y
                self.jumps = 0
                self.jump = False
                self.vertical_momentum = 0
                self.gravity = 0

    def animation(self, screen):
        if self.moving_right or self.moving_left:
            self.a.right(self.dt, self.facing_left)
        if self.jump:
            self.a.jump(self.dt)
        elif not self.moving_right and not self.moving_left:
            self.a.standing(self.facing_left) 
        self.sprite_group.draw(screen)

    def render(self, screen):
        if self.animate:
            self.animation(screen)
        else:
            pygame.draw.rect(screen, (255,0,0), self.rect)

    def update(self, dt, tiles=[]):
        self.move(dt)
        self.check_collisions(dt, tiles)