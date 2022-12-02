import sys
sys.path.append('../')
from core.config import *
from core.render import debug_msg
import pygame
from pygame.math import Vector2
from pygame.locals import *
from numpy import sign
from particles.particles import Particles, Sparks
from random import randint


class Animation(pygame.sprite.Sprite):
    def __init__(self, gravity, scale=4):
        super().__init__()
        self.n_animations = 0
        self.dividor = abs(gravity) * TICKRATE # doesn't work for now
        self.scaling = scale
        self.type = None

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
                        pass
                        #print(e) # inform which file does not exist
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
                self.type = type
                self.n_animations = values[1]
                self.sprites[type] = [self.n_animations, [], 0]
                self.sprites_flipped[type] = [self.n_animations, []]
                try:
                    self.sprite_sheet = pygame.image.load(values[0]).convert()
                except FileNotFoundError as e:
                    print(e)
                    continue
                size = list(self.sprite_sheet.get_size())
                scaling_size = (size[0] * self.scaling, size[1] * self.scaling)
                self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, scaling_size)
                self.sprite_WINDOWS_width = TILE_SIZE * self.scaling
                self.sprite_height = TILE_SIZE * self.scaling
                for x in range(self.n_animations):
                    self.sprites[type][1].append(self.get_sprite(x*self.sprite_WINDOWS_width, 0, self.sprite_WINDOWS_width, self.sprite_height))
                    self.sprites_flipped[type][1].append(pygame.transform.flip(self.sprites[type][1][x], True, False))
            self.rect = self.sprites[self.type][1][0].get_rect()  
        return True

    def get_sprite(self, x, y, w, h):
        sub = 85#(self.scaling * (TILE_SIZE - 64)) / 2 # static for now
        # sprite = pygame.Surface((w,h - sub))
        sprite = pygame.Surface(((TILE_SIZE)*self.scaling, (TILE_SIZE) * self.scaling))
        sprite.set_colorkey((255,255,255)) # turn it off to see player's rect
        sprite.blit(self.sprite_sheet, (0,0), (x, y, TILE_SIZE * self.scaling, TILE_SIZE*self.scaling))
        return sprite

    def update(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1] - TILE_SIZE * self.scaling + TILE_SIZE

    def animate(self, dt, facing_left, type):
        # if type not in self.sprites.keys(): return False
        # print(type)
        self.image = self.sprites[self.type][1][0]
        dt /= 10 # normalize
        if type == "stand":
            dt /= 3
        if type == 'jump':
            self.sprites[type][2] += self.sprites[type][0]/ 700 #(self.dividor * dt) #static for now
        else:
            try:
                self.sprites[type][2] += dt
            except Exception as e:
                #print(f"Animation {type} not found")
                return
        index = int(self.sprites[type][2]%self.sprites[type][0])
        try:
            if not facing_left:
                self.image = self.sprites[type][1][index]
                # print("sadf")
            else:
                self.image = self.sprites_flipped[type][1][index]
            if index+1 == self.sprites[type][0]:
                self.sprites[type][2] = 0
                return False
        except Exception as e:
            #print(f"Animation {type} not found")
            return
        # print(type, self.image)
        return True