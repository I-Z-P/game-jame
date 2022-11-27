# different camera models


import sys
sys.path.append('../')
from core.config import *
import pygame
from pygame.math import Vector2


class Camera():
    def __init__(self, display, model='follow_player'):
        self.display = display
        self.model = model
        self.half_w = self.display.get_size()[0] // 2
        self.half_h = self.display.get_size()[1] // 2
        self.position = Vector2()

    def static(self):
        pass

    def follow_player(self, player):
        player.position.x += ((WINDOW_WIDTH / 2) - player.position.x - TILE_SIZE/2)
        # player.position.y += ((WINDOW_HEIGHT / 2) - player.position.y - TILE_SIZE/2)
        player.rect = pygame.Rect(player.position.x, player.position.y, TILE_SIZE, TILE_SIZE)
        self.position.x += player.shift.x
        # self.position.y += player.shift.y


    def update(self, player):
        if self.model == 'static':
            pass
        elif self.model == 'follow_player':
            self.follow_player(player)
        else:
            pass