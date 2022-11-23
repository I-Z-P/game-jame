# loads a level map from .tmx file

import sys
sys.path.append('../')
from core.config import TILE_SIZE
import pygame, sys
from pytmx.util_pygame import load_pygame
pygame.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)


class Level():
    def __init__(self, file='./data/export/asdf.tmx'):
        self.soft_tiles = pygame.sprite.Group()     # tiles that do not collide with the player
        self.hard_tiles = pygame.sprite.Group()     # tiles that collide with the player
        self.tiles = self.load_level(file)

    def load_level(self, file='level/data/export/asdf.tmx'):
        tmx_data = load_pygame(file)
        for layer in tmx_data.visible_layers:
            print(layer.name)
            if hasattr(layer, 'data'):
                for x,y,surf in layer.tiles():
                    pos = (x* TILE_SIZE, y* TILE_SIZE)
                    # hard tiles
                    if layer.name == 'test1':
                        Tile(pos = pos, surf = surf, groups = self.hard_tiles)
                    # soft tiles
                    else:
                        Tile(pos = pos, surf = surf, groups = self.soft_tiles)

    def render(self, screen):
        level.soft_tiles.draw(screen)
        level.hard_tiles.draw(screen)


screen = pygame.display.set_mode((1280,720))
level = Level()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    level.render(screen)

    pygame.display.update()