import sys
sys.path.append('../')
from core.config import *
from core.render import debug_msg
import pygame
# from pygame.math import Vector2
# from pygame.locals import *
# from numpy import sign
# from particles.particles import Particles, Sparks
# from misc.stone import Stone
# from misc.animation import Animation
# from random import randint
from player.player import Player

class Enemy():
    def __init__(self, pos=[0,0], player_images=animations_wizard, type="agressive", hp=20):
        self.enemy = Player(pos, player_images)
        self.enemy.velocity = 2
        self.type = type
        self.hp = hp
    
    def update(self, game, dt):
        self.enemy.update(game, dt)

    def render(self, screen):
        self.enemy.render(screen)

    def move_towards(self, obj, space=80):
        if obj.position.x + space < self.enemy.position.x:
            self.enemy.attacking = False # too far from object
            self.enemy.go_left = True
        elif obj.position.x - space > self.enemy.position.x:
            self.enemy.go_right = True
            self.enemy.attacking = False
        else:
            self.enemy.go_left = False
            self.enemy.go_right = False
            self.attack(obj)

    def attack(self, obj):
        self.enemy.attacking = True

    def fight(self, obj):
        if self.type == 'agressive':
            self.move_towards(obj)