# launching the game and running game loop


from config import *
from events import *
from render import *
import pygame
pygame.init()


def game_loop(screen):
    clock = pygame.time.Clock()
    while True:
        clock.tick(TICKRATE)
        render(screen)
        handle_events()
        pygame.display.update()

def launch_the_game():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    game_loop(screen)


if __name__ == "__main__":
    launch_the_game()