# launching the game and running game loop

import sys
sys.path.append('../')
from player.player import Player
from level.level import Level
from config import *
from events import *
from render import *
import time
import pygame
pygame.init()


# pin update functions to run in each iteration here
def update(delta_time, player, level):
    # debug_msg(delta_time)
    player.update(delta_time, tiles=level.hard_tiles)


def game_loop(screen, level, player):
    print('been there')
    previous_time = time.time()
    while True:
        render(screen, player, level)
        delta_time = time.time() - previous_time
        previous_time = time.time()
        update(delta_time, player, level)
        handle_events(player)
        pygame.display.update()


def launch_the_game():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    level = Level()
    player = Player()
    game_loop(screen, level, player)


if __name__ == "__main__":
    launch_the_game()