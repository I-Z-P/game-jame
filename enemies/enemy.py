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
    def __init__(self, pos=[0,0], player_images=animations_wizard):
        self.enemy = Player(pos, player_images)
        self.enemy.facing_left = True
        # self.player_images = animations_wizard
        # self.pos = pos
    
    def update(self, game, dt):
        self.enemy.update(game, dt)

    def render(self, screen):
        self.enemy.render(screen)