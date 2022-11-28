# handling keyboard events and calling the corresponding functions


import pygame
from config import *
import sys
sys.path.append('../')
from ui.menu import In_game_menu


def keyboard_assignments(event, screen, player, game):
    if DEV: print('Pressed key in ascii:', event.key) 
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        in_game_menu = In_game_menu(game.screen, game)
        in_game_menu.loop()
    if pressed_keys[pygame.K_LEFT]:
        player.move_left()
    if pressed_keys[pygame.K_RIGHT]:
        player.move_right()
    if pressed_keys[pygame.K_UP]:
        player.move_up()

def handle_events(game):
    screen = game.screen
    player = game.player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            keyboard_assignments(event, screen, player, game)
        # temporarly added in order to fix player movement
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.jump = False
            elif event.key == pygame.K_RIGHT:
                player.moving_right = False
            elif event.key == pygame.K_LEFT:
                player.moving_left = False