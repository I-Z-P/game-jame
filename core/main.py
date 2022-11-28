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


class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.level = Level()
        self.player = Player()
        self.camera = Camera(self.screen)
        self.launch_the_game()

    # pin update functions to run in each iteration here
    def update(self, delta_time):
        # debug_msg(delta_time)
        self.player.update(delta_time, tiles=self.level.hard_tiles)
        self.camera.update(self.player)

    def loop(self):
        previous_time = time.time()
        while True:
            render(self.screen, self.player, self.level, self.camera)
            delta_time = time.time() - previous_time
            previous_time = time.time()
            self.update(delta_time)
            handle_events(self.screen, self.player)
            pygame.display.update()

    def launch_the_game(self):
        if not DEV:
            menu = Menu(self.screen)
            menu.launch_menu()
            fade_in_transition(self.screen, lambda: render(self.screen, self.player, self.level, self.camera))
        self.loop()


if __name__ == "__main__":
    Game()