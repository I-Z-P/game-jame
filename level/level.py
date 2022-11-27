# loads a level map from .tmx file

import sys
sys.path.append('../')
from core.config import *
import pygame
from pygame.math import Vector2
from pytmx.util_pygame import load_pygame
pygame.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self, offset, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.offset = offset
        self.position = self.offset
        self.rect = self.image.get_rect(topleft = self.position)

    def update(self, camera):
        self.position = Vector2(self.offset.x - camera.position.x, self.offset.y - camera.position.y)
        self.rect = self.image.get_rect(topleft = self.position)


class Level():
    def __init__(self, file=ROOT_PATH+'/level/data/export/asdf.tmx'):
        self.soft_tiles = pygame.sprite.Group()     # tiles that do not collide with the player
        self.hard_tiles = pygame.sprite.Group()     # tiles that collide with the player
        self.tiles = self.load_level(file)

    def load_level(self, file=ROOT_PATH+'/level/data/export/asdf.tmx'):
        tmx_data = load_pygame(file)
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x,y,surf in layer.tiles():
                    offset = Vector2(x*TILE_SIZE, y*TILE_SIZE)
                    # hard tiles
                    if layer.name == 'test1':
                        Tile(offset = offset, surf = surf, groups = self.hard_tiles)
                    # soft tiles
                    else:
                        Tile(offset = offset, surf = surf, groups = self.soft_tiles)

    def render(self, screen, camera):
        self.soft_tiles.update(camera)
        self.hard_tiles.update(camera)
        self.soft_tiles.draw(screen)
        self.hard_tiles.draw(screen)