# main menu screen and all related functions


import sys
sys.path.append('../')
from core.config import *
import pygame
from pygame.math import Vector2
pygame.init()


class Button():
    def __init__(self, pos, text=None, image=None, image_hover=None):
        self.position = Vector2(pos)
        self.text = text
        self.font = pygame.font.Font(str(ROOT_PATH + '/ui/font.ttf'), 70)
        self.font_color = (0,0,0)
        self.font_color_hover = (76, 88, 94)
        if image:
            self.surface = pygame.image.load(image).convert_alpha()
        else:
            self.surface = self.font.render(self.text, True, self.font_color)
        if image_hover:
            self.surface_hover = pygame.image.load(image_hover).convert_alpha()
        else:
            self.surface_hover = self.font.render(self.text, True, self.font_color_hover)
        self.rect = self.surface.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.is_hovered = False

    def render(self, screen, mouse):
        if self.rect.collidepoint(mouse):
            self.is_hovered = True
        else:
            self.is_hovered = False
        if self.is_hovered:
            screen.blit(self.surface_hover, self.position)
        else:
            screen.blit(self.surface, self.position)


class Menu():
    def __init__(self):
        self.open = True
        self.background_color = (138, 151, 171)
        self.start_button = Button(pos=[WINDOW_WIDTH/6, WINDOW_HEIGHT/10*5], text="Start", image=None, image_hover=None)
        self.settings_button = Button(pos=[WINDOW_WIDTH/6, WINDOW_HEIGHT/10*6], text="Settings", image=None, image_hover=None)
        self.exit_button = Button(pos=[WINDOW_WIDTH/6, WINDOW_HEIGHT/10*7], text="Exit", image=None, image_hover=None)
        self.buttons = [self.start_button, self.settings_button, self.exit_button]

    def events(self, mouse):
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if pressed_keys[pygame.K_ESCAPE]:
                    self.open = False
                    if DEV: print('Escape menu')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.rect.collidepoint(mouse):
                    if DEV: print('Start button clicked')
                    self.open = False
                elif self.exit_button.rect.collidepoint(mouse):
                    if DEV: print('Exit button clicked')
                    pygame.quit()
                elif self.settings_button.rect.collidepoint(mouse):
                    if DEV: print('Settings button clicked')

    def loop(self, screen):
        while self.open:
            mouse = pygame.mouse.get_pos()
            self.events(mouse)
            screen.fill(self.background_color)
            for button in self.buttons:
                button.render(screen, mouse)
            pygame.display.update()


if __name__ == "__main__":
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    menu = Menu()
    menu.loop(screen)