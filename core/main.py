# launching the game and running game loop

import sys
sys.path.append('../')
from player.player import Player
from enemies.enemy import Enemy
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
        self.fps_counter = Fps_counter(self.screen)
        self.launch_the_game()

    # pin update functions to run in each iteration here
    def update(self, delta_time):
        # debug_msg(delta_time)
        for obj in self.objects:
            obj.update(self, delta_time)
            if obj.type == "agressive":
                obj.fight(self.player)
        self.camera.update(self.objects[1].enemy)

    def loop(self):
        previous_time = time.time()
        while True:
            delta_time = time.time() - previous_time
            previous_time = time.time()
            self.update(delta_time)
            render(self.screen, self.objects, self.level, self.camera, self.fps_counter)
            pygame.display.update()
            handle_events(self)
            if FPS_COUNTER:
                self.fps_counter.clock.tick(TICKRATE)

    def launch_the_game(self):
        if not DEV:
            menu = Menu(self.screen, self)
            menu.launch_menu()
        self.new_game()

    def new_game(self):
        self.level = Level()
        self.player = Player()
        self.objects = [self.player, Enemy([1800,0], animations_knight)]
        self.camera = Camera(self.screen)
        if not DEV:
            fade_in_transition(self.screen, lambda: render(self.screen, self.player, self.level, self.camera, self.fps_counter))
        self.loop()

    def enter_cave(self, position, rect, alpha=255):
        return enter_cave(self.screen, lambda: render(self.screen, self.player, self.level, self.camera, self.fps_counter), alpha, position, rect, radius=900)


if __name__ == "__main__":
    Game()