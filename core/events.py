# handling keyboard events and calling the corresponding functions


import pygame
from config import *
import sys
sys.path.append('../')
from ui.menu import In_game_menu


def keyboard_assignments(pressed_keys, game):
    if pressed_keys[pygame.K_ESCAPE]:
        if DEV:
            sys.exit()
        in_game_menu = In_game_menu(game.screen, game)
        in_game_menu.loop()
    if pressed_keys[pygame.K_LEFT]:
        game.player.go_left = True
    if pressed_keys[pygame.K_RIGHT]:
        game.player.go_right = True
    if pressed_keys[pygame.K_UP]:
        game.player.go_up = True
    if pressed_keys[pygame.K_DOWN]:
        # game.player.roll()
        pass
    if pressed_keys[pygame.K_SPACE]:
        game.player.attacking = True
    if pressed_keys[pygame.K_s]:
        # game.player.shield()
        pass


def handle_events(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if DEV: print('Closing')
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed_buttons = pygame.mouse.get_pressed()
            if DEV: print('Mouse clicked:', pressed_buttons)
            # if pressed_buttons[0]:  # left mouse button
            #     game.player.attack()
            # if pressed_buttons[2]:  # right mouse button
            #     game.player.shield()
        if event.type == pygame.KEYDOWN:
            if DEV: print('Pressed key:', pygame.key.name(event.key))
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys:
        keyboard_assignments(pressed_keys, game)