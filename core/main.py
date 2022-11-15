# launching the game and running game loop

import sys
sys.path.append('../')
from player.player import Player
from config import *
from events import *
from render import *
import time
import pygame
pygame.init()


# pin update functions to run in each iteration here
def update(delta_time, player):
    # debug_msg(delta_time)
    player.update(delta_time)


def game_loop(screen):
    player = Player()
    previous_time = time.time()
    while True:
        render(screen, player)
        delta_time = time.time() - previous_time
        previous_time = time.time()
        update(delta_time, player)
        handle_events(player)
        pygame.display.update()


def launch_the_game():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    game_loop(screen)


if __name__ == "__main__":
    launch_the_game()