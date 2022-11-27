# main menu screen and all related functions


import sys
sys.path.append('../')
from core.config import *
import pygame
from pygame.math import Vector2
pygame.init()


class Button():
    def __init__(self, pos, on_click, text=None, image=None, image_hover=None, is_hovered=False):
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
        self.is_hovered = is_hovered
        self.on_click = on_click

    def render(self, screen):
        if self.is_hovered:
            screen.blit(self.surface_hover, self.position)
        else:
            screen.blit(self.surface, self.position)


class Menu():
    def __init__(self):
        self.open = True
        self.background_color = (138, 151, 171)
        self.start_button = Button(pos=[WINDOW_WIDTH/6, WINDOW_HEIGHT/10*5], on_click=self.start, text="Start", image=None, image_hover=None, is_hovered=True)
        self.settings_button = Button(pos=[WINDOW_WIDTH/6, WINDOW_HEIGHT/10*6], on_click=self.settings, text="Settings", image=None, image_hover=None)
        self.exit_button = Button(pos=[WINDOW_WIDTH/6, WINDOW_HEIGHT/10*7], on_click=self.exit_game, text="Exit", image=None, image_hover=None)
        self.buttons = [self.start_button, self.settings_button, self.exit_button]
        self.hovered_button = 0   # index in self.buttons

    def events(self, mouse):
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if pressed_keys[pygame.K_ESCAPE]:
                    self.open = False
                    if DEV: print('Escape menu')
                if pressed_keys[pygame.K_DOWN]:
                    self.hover_next()
                if pressed_keys[pygame.K_UP]:
                    self.hover_previous()
                if pressed_keys[pygame.K_RETURN]:
                    self.buttons[self.hovered_button].on_click()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.buttons[self.hovered_button].on_click()

    def start(self):
        if DEV: print('Start button clicked')
        self.open = False

    def settings(self):
        if DEV: print('Settings button clicked')

    def exit_game(self):
        if DEV: print('Exit button clicked')
        self.open = False
        pygame.quit()
        sys.exit()

    def hover_next(self):
        if self.hovered_button < len(self.buttons)-1:
            self.hovered_button += 1

    def hover_previous(self):
        if self.hovered_button > 0:
            self.hovered_button -= 1

    def loop(self, screen):
        while self.open:
            mouse = pygame.mouse.get_pos()
            screen.fill(self.background_color)
            for button in self.buttons:
                button.is_hovered = False
                if button.rect.collidepoint(mouse):
                    self.hovered_button = self.buttons.index(button)
            self.buttons[self.hovered_button].is_hovered = True
            self.events(mouse)
            for button in self.buttons:
                button.render(screen)
            pygame.display.update()


if __name__ == "__main__":
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    menu = Menu()
    menu.loop(screen)