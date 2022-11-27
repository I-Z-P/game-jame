# launching the game and running game loop

import sys
sys.path.append('../')
from player.player import Player
from level.level import Level
from level.camera import Camera
from ui.menu import Menu
from misc.fade_transition import *
from config import *
from events import *
from render import *
import time
import pygame
pygame.init()


# pin update functions to run in each iteration here
def update(delta_time, player, level, camera):
    # debug_msg(delta_time)
    player.update(delta_time, tiles=level.hard_tiles)
    camera.update(player)


def game_loop(screen, level, player, camera):
    previous_time = time.time()
    while True:
        render(screen, player, level, camera)
        delta_time = time.time() - previous_time
        previous_time = time.time()
        update(delta_time, player, level, camera)
        handle_events(player)
        pygame.display.update()


def launch_the_game():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    if not DEV:
        menu = Menu()
        menu.launch_menu(screen)
    level = Level()
    player = Player()
    camera = Camera(screen)
    if not DEV:
        fade_in_transition(screen, lambda: render(screen, player, level, camera))
    game_loop(screen, level, player, camera)


if __name__ == "__main__":
    launch_the_game()