# launching the game and running game loop


from config import *
from events import *
from render import *
import time
import pygame
pygame.init()


# pin update functions to run in each iteration here
def update(delta_time):
    # debug_msg(delta_time)
    pass


def game_loop(screen):
    previous_time = time.time()
    while True:
        render(screen)
        delta_time = time.time() - previous_time
        previous_time = time.time()
        update(delta_time)
        handle_events()
        pygame.display.update()


def launch_the_game():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    game_loop(screen)


if __name__ == "__main__":
    launch_the_game()