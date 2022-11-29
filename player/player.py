# this file contain Player class

import sys
sys.path.append('../')
from core.config import *
import pygame
from pygame.math import Vector2
from pygame.locals import *
from numpy import sign
from particles.particles import Particles 


class Animation(pygame.sprite.Sprite):
    def __init__(self, gravity, scale=2):
        super().__init__()
        self.n_animations = 0
        self.dividor = abs(gravity) * TICKRATE # doesn't work for now
        self.scaling = scale

    def load_player_body(self, player_images=[], sprite_sheet=False):
        self.sprites = []
        if not sprite_sheet:
            if player_images:
                for image_name in player_images:
                    try:
                        sprite = pygame.image.load(image_name + ".png").convert()
                        sprite.set_colorkey((255, 255, 255))
                        sprite = pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
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
                self.sprites[type] = [self.n_animations, [], 0]
                self.sprites_flipped[type] = [self.n_animations, []]
                try:
                    self.sprite_sheet = pygame.image.load(values[0]).convert()
                except FileNotFoundError as e:
                    print(e)
                    continue
                size = list(self.sprite_sheet.get_size())
                scaling_size = (TILE_SIZE * self.scaling * self.n_animations, TILE_SIZE * self.scaling)
                self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, scaling_size)
                self.sprite_width = TILE_SIZE * self.scaling
                self.sprite_height = TILE_SIZE * self.scaling
                for x in range(self.n_animations):
                    self.sprites[type][1].append(self.get_sprite(x*self.sprite_width, 0, self.sprite_width, self.sprite_height))
                    self.sprites_flipped[type][1].append(pygame.transform.flip(self.sprites[type][1][x], True, False))
            self.rect = self.sprites['run'][1][0].get_rect()  
        return True

    def get_sprite(self, x, y, w, h):
        sub = 85#(self.scaling * (TILE_SIZE - 64)) / 2 # static for now
        sprite = pygame.Surface((w,h - sub))
        sprite.set_colorkey((0,0,0)) # turn it off to see player's rect
        sprite.blit(self.sprite_sheet, (0,0), (x, y, w, h))
        return sprite

    def animate(self, dt, facing_left, type):
        dt /= 10 # normalize
        if type == 'jump':
            self.sprites[type][2] += self.sprites[type][0]/ 200 #(self.dividor * dt) #static for now
        else:
            try:
                self.sprites[type][2] += dt
            except Exception as e:
                print(f"Animation {type} not found")
                return
        index = int(self.sprites[type][2]%self.sprites[type][0])
        try:
            if not facing_left:
                self.image = self.sprites[type][1][index]
            else:
                self.image = self.sprites_flipped[type][1][index]
            if index+1 == self.sprites[type][0]:
                self.sprites[type][2] = 0
                return False
        except Exception as e:
            print(f"Animation {type} not found")
            return
        return True


class Player():
    def __init__(self, gravity=5, max_jumps=1, starting_position=[WINDOW_WIDTH//2,0], acceleration=[1,0], max_velocity=5, player_images=animations_wizard):
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
        self.go_right = False
        self.go_left = False
        self.go_up = False
        self.pressing = False
        self.on_ground = False
        self.attacking = False
        self.shielding = False
        self.rolling = False
        self.particle_effect = False
        self.p = Particles()
        self.color = (41,7,47)

    def initialize_animation(self, player_images):
        self.a = Animation(self.gravity)
        if self.a.load_player_body(player_images, type(player_images) is dict):
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

    def attack(self):
        self.attacking = True
        if not self.particle_effect:
            self.p.load_particles(100,position=(self.rect.x + self.rect.w/2 + 20, self.rect.y + 80), color=self.color, velocity=(sign(int(self.facing_left)-1) * -2,2))
        self.particle_effect = True
    
    def shield(self):
        self.shielding = True

    def roll(self):
        self.rolling = True

    def move(self, dt):
        dt *= 100 # normalize
        self.dt = dt
        self.shift = Vector2(0, 0)
        if abs(self.velocity.x) <= self.max_velocity: # if boundry of max velocity is not crossed
            if self.acceleration.x == 0: self.acceleration.x = self.base_acceleration[0] # if acceleration is turned off then turn it on
            if self.go_right:
                self.facing_left = False
                self.velocity.x += self.acceleration.x * dt
            if self.go_left:
                self.facing_left = True
                self.velocity.x -= self.acceleration.x * dt
            if self.go_left and self.go_right or not self.go_left and not self.go_right:
                if abs(self.velocity.x) < abs(self.acceleration.x): self.velocity.x = 0
                else:
                    self.velocity.x += -sign(self.velocity.x) * self.acceleration.x/10
        else:
            self.acceleration.x = 0
            self.velocity.x = sign(self.velocity.x) * self.max_velocity
        self.shift.x += self.velocity.x * dt
        self.position.x += self.shift.x
        if self.go_up:
            if self.jumps < self.max_jumps and not self.pressing:
                self.vertical_momentum = -self.gravity
                self.jumps += 1
                self.pressing = True # initialize space pressing
        else:
            self.pressing = False # user stopped pressing space
        if not self.on_ground:
            self.vertical_momentum += self.gravity/100
            if self.vertical_momentum > self.gravity:
                self.vertical_momentum = self.gravity
        else:
            self.shift.y += 1
        self.shift.y += self.vertical_momentum * dt
        self.position.y += self.shift.y

    def check_collisions(self, dt, tiles):
        self.rect.x = self.position.x
        collisions = self.collide(tiles)
        for tile in collisions:
            self.acceleration.x = 0
            if self.go_right:
                self.position.x = tile.rect.x - TILE_SIZE
                self.rect.x = self.position.x
            elif self.go_left:
                self.position.x = tile.rect.x + TILE_SIZE
                self.rect.x = self.position.x
        self.rect.y = self.position.y
        collisions = self.collide(tiles)
        if collisions:
            for tile in collisions:
                if self.vertical_momentum < 0:
                    self.position.y += (self.position.y % TILE_SIZE)
                    self.rect.y = self.position.y
                    self.vertical_momentum = 0
                else:
                    self.position.y = tile.rect.top - self.rect.h
                    self.rect.y = self.position.y
                    self.jumps = 0
                    self.go_up = False
                    self.vertical_momentum = 0
                    self.on_ground = True
        else:
            self.on_ground = False

    def animation(self, screen):
        self.particle_effect = self.p.splash(self.dt, screen)
        if self.go_right or self.go_left:
            type = 'run'
        if self.go_up:
            type = 'jump'
        elif not self.go_right and not self.go_left:
            type = 'stand'
        if self.rolling:
            type = 'roll'
            self.rolling = self.a.animate(self.dt, self.facing_left, type)
        elif self.attacking:
            type = 'attack'
            self.attacking = self.a.animate(self.dt, self.facing_left, type)
        elif self.shielding:
            type = 'shield'
            self.shielding = self.a.animate(self.dt, self.facing_left, type)
        else:
            self.a.animate(self.dt, self.facing_left, type)
        self.sprite_group.draw(screen)

    def render(self, screen):
        if self.animate:
            self.animation(screen)
        else:
            pygame.draw.rect(screen, (255,0,0), self.rect)

    def update(self, dt, tiles=[]):
        self.move(dt)
        self.check_collisions(dt, tiles)