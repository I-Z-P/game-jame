# this file contain Player class

import sys
sys.path.append('../')
import pygame
from pygame.math import Vector2
from pygame.locals import *
from numpy import sign
from core.config import *


class Animation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.n_animations = 0

    def load_player_body(self, player_images=[]):
        self.sprites = []
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
            self.rect = pygame.Rect(0,0,TILE_SIZE/4,TILE_SIZE/2)
            return False
        return True

    def right(self, dt):
        dt /= 10 # normalize
        self.current_running_sprite += dt
        self.image = self.sprites[int(self.current_running_sprite%self.n_animations)]

    def left(self, dt):
        dt /= 10 # normalize
        self.current_running_sprite += dt
        self.image = self.sprites_flipped[int(self.current_running_sprite%self.n_animations)]

    def standing(self, facing_left):
        if facing_left:
            self.image = self.sprites_flipped[0]
        else:
            self.image = self.sprites[0]


class Player():
    def __init__(self, gravity=8, max_jumps=1, starting_position=[0,0], acceleration=[0.2,0], max_velocity=5, player_images=[]):
        self.base_acceleration = acceleration
        self.max_velocity = abs(max_velocity)
        self.gravity = gravity
        self.vertical_momentum = 0
        self.max_jumps = max_jumps
        self.jumps = 0 # jumps counter
        self.position = Vector2(starting_position) # player's position
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
        if self.a.load_player_body(player_images):
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
        self.moving_right = False

    def move_right(self):
        self.moving_left = False
        self.moving_right = True

    def move_up(self):
        self.jump = True

    def move(self, dt):
        dt *= 100 # normalize
        self.dt = dt
        if abs(self.velocity.x) <= self.max_velocity: # if boundry of max velocity is not crossed
            if self.acceleration.x == 0: self.acceleration.x = self.base_acceleration[0] # if acceleration is turned off then turn it on
            if self.moving_right:
                self.facing_left = False
                #self.animate = True
                self.velocity += self.acceleration * dt
            elif self.moving_left:
                self.facing_left = True
                #self.animate = True
                self.velocity -= self.acceleration * dt
            else:
                if abs(self.velocity.x) < abs(self.acceleration.x): self.velocity.x = 0
                else:
                    self.velocity.x += -sign(self.velocity.x) * self.acceleration.x/self.gravity
        else:
            self.acceleration.x = 0
            self.velocity.x = sign(self.velocity.x) * self.max_velocity
        self.position.x += self.velocity.x * dt
        if self.jump:
            if self.jumps < self.max_jumps and not self.pressing:
                self.vertical_momentum = -self.gravity#-4 # static jump for now
                self.jumps += 1
                self.pressing = True # initialize space pressing
        else:
            self.pressing = False # user stopped pressing space
        self.vertical_momentum += dt/self.gravity
        if self.vertical_momentum > self.gravity:
            self.vertical_momentum = self.gravity
        self.position.y += self.vertical_momentum * dt
        self.rect.x = self.position.x

    def check_collisions(self, dt, tiles):
        collisions = self.collide(tiles)
        for tile in collisions:
            if self.moving_right:
                self.position.x -= self.velocity.x * dt
                self.rect.x = self.position.x
            elif self.moving_left:
                self.position.x += self.velocity.x * dt
                self.rect.x = self.position.x
        self.rect.y = self.position.y
        collisions = self.collide(tiles)
        for tile in collisions:
            if self.vertical_momentum < 0:
                self.position.y = tile.rect.bottom
                self.rect.y = self.position.y
                self.vertical_momentum = self.gravity/10
            else:
                self.position.y = (tile.rect.top - self.rect.h)
                self.rect.y = self.position.y
                self.jumps = 0
                self.vertical_momentum = 0

    def animation(self, screen):
        if self.moving_right:
            self.a.right(self.dt)
        elif self.moving_left:
            self.a.left(self.dt)
        else:
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