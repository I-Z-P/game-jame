# different camera models


import sys
sys.path.append('../')
from core.config import *
import pygame
from pygame.math import Vector2


class Camera():
    def __init__(self, display, model='static'):
        self.display = display
        self.model = model
        self.half_w = self.display.get_size()[0] // 2
        self.half_h = self.display.get_size()[1] // 2
        self.position = Vector2()

    def static(self):
        pass

    def follow_player(self, player, delay=10):
        player.position.x += ((WINDOW_WIDTH / 2) - player.position.x - TILE_SIZE/2) / delay
        if player.on_gorund:
            player.position.y -= player.position.y % TILE_SIZE
        player.rect = pygame.Rect(player.position.x, player.position.y, TILE_SIZE, TILE_SIZE)
        self.position.x += player.shift.x
        self.position.y = player.position.y
        self.position.y += (self.position.y % TILE_SIZE)

    def update(self, player):
        if self.model == 'static':
            pass
        elif self.model == 'follow_player':
            self.follow_player(player)
        else:
            pass