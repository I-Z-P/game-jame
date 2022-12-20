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
    def __init__(self, pos=[1000,0], player_images=animations_knight, hp=100):
        self.position = Vector2(pos)
        self.shift = Vector2(0, 0)
        self.jump_velocity = 10
        self.gravity = 10
        self.max_jump = 200
        self.jump_count = 0
        self.jump_height = 0
        self.velocity = 7
        self.color = (0,0,0)
        self.rect = pygame.Rect(self.position.x, self.position.y, TILE_SIZE, TILE_SIZE)
        self.go_left = False
        self.go_right = False
        self.go_up = False
        self.on_gorund = False
        self.jumping = False
        self.falling = True
        self.collisions = {'left' : False, 'right' : False, 'top' : False, 'bottom' : False}
        self.initialize_animation(player_images)
        self.attacking = False
        self.dt = 0
        self.type = 'player'
        self.hp = hp
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
        self.shift = Vector2(0, 0)
        self.running = False
        # left / right section
        if self.go_left:
            self.done = False
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
        # jump section
        if self.go_up:
            self.test_collisions(pygame.Rect(self.position.x, self.position.y + 1, TILE_SIZE, TILE_SIZE), level.hard_tiles)
            if self.collisions['bottom']:
                self.jump_count += 1
                self.jumping = True
                self.jump_height = 0
                self.go_up = False
            self.test_collisions(pygame.Rect(self.position.x, self.position.y - 1, TILE_SIZE, TILE_SIZE), level.hard_tiles)
            if self.collisions['top']:
                self.jumping = False
                self.falling = True
                self.jump_height = 0
                self.go_up = False
            if self.jump_height >= self.max_jump:
                self.jumping = False
                self.falling = True
                self.jump_height = 0
                self.go_up = False
            if self.jumping:
                self.shift.y -= self.jump_velocity * dt
                self.jump_height += self.jump_velocity * dt
            self.velocity = 7
        # gravity section
        self.test_collisions(pygame.Rect(self.position.x, self.position.y + 1, TILE_SIZE, TILE_SIZE), level.hard_tiles)
        if self.collisions['bottom']:
            self.on_gorund = True
            self.falling = False
            self.jump_count = 0
            if int(self.position.y % TILE_SIZE) > 0:
                self.position.y -= (self.position.y % TILE_SIZE)
        if self.falling:
            self.shift.y += self.jump_velocity * dt

        # new position
        self.position += self.shift
        self.rect = pygame.Rect(self.position.x, self.position.y, TILE_SIZE, TILE_SIZE)

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
                    # self.jumping = False

    def got_hit(self, obj, space=30):
        self.test_collisions(pygame.Rect(self.position.x + space, self.position.y, TILE_SIZE, TILE_SIZE), [obj.enemy])
        if self.collisions['right']:
            print("hit")
            self.go_left = True
            self.velocity = 100
            return True
        self.test_collisions(pygame.Rect(self.position.x - space, self.position.y, TILE_SIZE, TILE_SIZE), [obj.enemy])
        if self.collisions['left']:
            self.velocity = 100
            print("hit")
            self.go_right = True
            return True
        return False

    def check_death(self):
        if self.position.y > WINDOW_HEIGHT:
            if not self.done:
                self.s = game.enter_cave(self.position, self.rect)
                self.done = True

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
            # print(self.test_collisions(self.rect, ))
        elif not self.attacking:
            self.a.animate(self.dt, self.facing_left, type)
        #self.stone.update(screen)
        self.a.update(self.position)
        self.sprite_group.draw(screen)

    def render(self, screen):
        if self.animate:
            self.animation(screen)
            try:
                screen.blit(self.s, (0,0))
            except:
                pass
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def enter_cave(self, screen):
        self.s = game.enter_cave(self.position, self.rect)

    def update(self, game, dt):
        self.move(dt, game.level)