# this file contain Player class

import sys
sys.path.append('../')
from core.config import *
from core.render import debug_msg
import pygame
from pygame.math import Vector2
from pygame.locals import *
from numpy import sign
from particles.particles import Particles, Sparks
from misc.stone import Stone
from misc.animation import Animation
from random import randint


class Player():
    def __init__(self, pos=[0,0], player_images=animations_knight):
        self.position = Vector2(pos)
        self.shift = Vector2(0, 0)
        self.jump = Vector2(0, 0)
        self.gravity = 15
        self.velocity = 7
        self.color = (0,0,0)
        self.rect = pygame.Rect(self.position.x, self.position.y, TILE_SIZE, TILE_SIZE)
        self.go_left = False
        self.go_right = False
        self.go_up = False
        self.on_gorund = False
        self.collisions = {'left' : False, 'right' : False, 'top' : False, 'bottom' : False}
        self.initialize_animation(player_images)
        self.attacking = False
        self.dt = 0
        self.jumping = False

        #self.stone = Stone("#a7180c")

    def initialize_animation(self, player_images):
        self.a = Animation(self.gravity)
        if self.a.load_player_body(player_images, type(player_images) is dict):
            self.animate = True
        else:
            self.animate = False
        self.a.rect = self.rect
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.a)
        self.facing_left = False   


    def move(self, dt, level):
        dt *= 100 # normalize
        self.dt = dt
        self.shift = Vector2(0, self.gravity)*dt
        self.position.y = int(self.position.y)
        self.running = False
        # left / right section
        if self.go_left:
            self.facing_left = True
            self.go_left = False
            self.running = True
            self.test_collisions(pygame.Rect(self.position.x - 1, self.position.y, TILE_SIZE, TILE_SIZE), level.hard_tiles)
            if not self.collisions['left']:
                self.shift += Vector2(-self.velocity, 0)*dt
            else:
                self.position.x -= self.position.x % TILE_SIZE
        if self.go_right:
            self.facing_left = False
            self.go_right = False
            self.running = True
            self.test_collisions(pygame.Rect(self.position.x + self.velocity, self.position.y, TILE_SIZE, TILE_SIZE), level.hard_tiles)
            if not self.collisions['right']:
                self.shift += Vector2(self.velocity, 0)*dt
            else:
                if self.position.x % TILE_SIZE:
                    self.position.x += TILE_SIZE - (self.position.x % TILE_SIZE)
        # gravity section
        self.test_collisions(pygame.Rect(self.position.x, self.position.y + 1, TILE_SIZE, TILE_SIZE), level.hard_tiles)
        if self.collisions['bottom']: 
            self.on_gorund = True
            self.shift -= Vector2(0, self.gravity)*dt
            if int(self.position.y % TILE_SIZE) > 0:
                self.position.y -= (self.position.y % TILE_SIZE)
        # jump section
        if self.go_up:
            self.jumping = True
            self.go_up = False
            self.test_collisions(pygame.Rect(self.position.x, self.position.y + 1, TILE_SIZE, TILE_SIZE), level.hard_tiles)
            if self.collisions['bottom']:
                self.jump = Vector2(0, -40)
        self.test_collisions(pygame.Rect(self.position.x, self.position.y, TILE_SIZE, TILE_SIZE), level.hard_tiles)
        if self.jump.y > self.gravity or self.collisions['top']:
            self.jump = Vector2(0, 0)
        else: 
            self.on_gorund = False
            self.jump *= 0.9
            self.shift += self.jump
        # new position
        self.position += self.shift
        self.rect = pygame.Rect(self.position.x, self.position.y, TILE_SIZE, TILE_SIZE)
        # print(self.collisions)

    def test_collisions(self, hit_box, tiles):
        self.collisions = {'left' : False, 'right' : False, 'top' : False, 'bottom' : False}
        for tile in tiles:
            if hit_box.colliderect(tile.rect):
                if hit_box.x <= tile.rect.x:
                    self.collisions['right'] = True
                if hit_box.x >= tile.rect.x:
                    self.collisions['left'] = True
                if hit_box.y >= tile.rect.y:
                    self.collisions['top'] = True
                if hit_box.y <= tile.rect.y:
                    self.collisions['bottom'] = True
                    self.jumping = False

    def check_death(self):
        if self.position.y > WINDOW_HEIGHT:
            pass

    def animation(self, screen):
        # self.particle_effect = self.p.splash(screen)
        # self.sparking = self.s.fire(self.dt, screen)
        if self.running:
            type = 'run'
        if self.jumping:
            type = 'jump'

        elif not self.running:
            type = 'stand'
        if self.attacking:
            type = 'attack'
            self.attacking = self.a.animate(self.dt, self.facing_left, type)
        elif not self.attacking:
            self.a.animate(self.dt, self.facing_left, type)
        #self.stone.update(screen)
        self.a.update(self.position)
        self.sprite_group.draw(screen)

    def render(self, screen):
        if self.animate:
            self.animation(screen)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def update(self, game, dt):
        self.move(dt, game.level)