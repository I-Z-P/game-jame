# this file contain Player class

import sys
sys.path.append('../')
from core.config import *
from core.render import debug_msg
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
                self.sprite_WINDOWS_width = TILE_SIZE * self.scaling
                self.sprite_height = TILE_SIZE * self.scaling
                for x in range(self.n_animations):
                    self.sprites[type][1].append(self.get_sprite(x*self.sprite_WINDOWS_width, 0, self.sprite_WINDOWS_width, self.sprite_height))
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
    def __init__(self, pos=[0,0]):
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
        self.collisions = {'left' : False, 'right' : False, 'top' : False, 'bottom' : False}

    def move(self, dt, level):
        dt *= 100 # normalize
        print(dt)
        self.shift = Vector2(0, self.gravity)*dt
        self.position.y = int(self.position.y)
        # left / right section
        if self.go_left:
            self.go_left = False
            self.test_collisions(pygame.Rect(self.position.x - 1, self.position.y, TILE_SIZE, TILE_SIZE), level.hard_tiles)
            if not self.collisions['left']:
                self.shift += Vector2(-self.velocity, 0)*dt
        if self.go_right:
            self.go_right = False
            self.test_collisions(pygame.Rect(self.position.x + 1, self.position.y, TILE_SIZE, TILE_SIZE), level.hard_tiles)
            if not self.collisions['right']:
                self.shift += Vector2(self.velocity, 0)*dt
        # gravity section
        self.test_collisions(pygame.Rect(self.position.x, self.position.y + self.gravity, TILE_SIZE, TILE_SIZE), level.hard_tiles)
        if self.collisions['bottom']: 
            self.shift -= Vector2(0, self.gravity)*dt
            if self.position.y % TILE_SIZE > 0:
                self.position.y += TILE_SIZE - (self.position.y % TILE_SIZE)
        # jump section
        if self.go_up:
            self.go_up = False
            self.test_collisions(pygame.Rect(self.position.x, self.position.y + self.gravity, TILE_SIZE, TILE_SIZE), level.hard_tiles)
            if self.collisions['bottom']:
                self.jump = Vector2(0, -80)
        self.test_collisions(pygame.Rect(self.position.x, self.position.y - 1, TILE_SIZE, TILE_SIZE), level.hard_tiles)
        if self.jump.y > self.gravity or self.collisions['top']:
            self.jump = Vector2(0, 0)
        else: 
            self.jump *= 0.9
            self.shift += self.jump
        # new position
        self.position += self.shift
        # self.position.x += ((WINDOW_WIDTH / 2) - self.position.x)
        # print(self.shift)
        # print(self.position.x)
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

    def check_death(self):
        if self.position.y > WINDOW_HEIGHT:
            new_game()

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, game, dt):
        self.move(dt, game.level)