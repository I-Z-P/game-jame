# this file contain Player class

import pygame
from pygame.math import Vector2
from pygame.locals import *
from numpy import sign

class Player():
    def __init__(self, gravity=4, max_jumps=1, starting_position=[0,0], acceleration=[0.2,0], max_velocity=5, player_images=None):
        self.base_acceleration = acceleration
        self.max_velocity = abs(max_velocity)
        self.gravity = gravity
        self.vertical_momentum = 0
        self.max_jumps = max_jumps
        self.jumps = 0 # jumps counter
        self.position = Vector2(starting_position) # player's position
        self.velocity = Vector2([0,0]) # player's velocity
        self.acceleration = Vector2(self.base_acceleration) # player's acceleration
        self.model, self.rect = self.load_player_body(player_images)
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.pressing = False

    def load_player_body(self, player_images):
        if player_images: # if there are player images load them
            surfaces = []
            for image_name in player_images:
                surface = pygame.image.load(image_name).convert_alpha()
                surfaces.append(surface)
            return surfaces, surfaces[0].get_rect()
        else: # if there is no player images return simple rectangle shape
            surfaces = [None]
            rect = pygame.Rect(0,0,10,10)
            return surfaces, rect

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
        if abs(self.velocity.x) <= self.max_velocity: # if boundry of max velocity is not crossed
            if self.acceleration.x == 0: self.acceleration.x = self.base_acceleration[0] # if acceleration is turned off then turn it on
            if self.moving_right:
                self.velocity += self.acceleration * dt
            elif self.moving_left:
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
                self.vertical_momentum = -4 # static jump for now
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

    def render(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect)

    def update(self, dt, tiles=[]):
        self.move(dt)
        self.check_collisions(dt, tiles)