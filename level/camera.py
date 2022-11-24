# different camera models


import sys
sys.path.append('../')
from core.config import *
import pygame
from pygame.math import Vector2


class Camera():
    def __init__(self, display, model='player_in_center', x=0, y=0):
        self.display = display
        self.model = model
        self.half_w = self.display.get_size()[0] // 2
        self.half_h = self.display.get_size()[1] // 2
        self.position = Vector2(x, y)

    def update(self, player):
        if self.model == 'static':
            pass
        elif self.model == 'player_in_center':
            self.position = Vector2(player.rect.centerx - self.half_w, player.rect.centery - self.half_h)
            print(self.position)
            print(player.position)
        else:
            pass