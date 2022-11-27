# fade transition efect between two stages


import sys
sys.path.append('../')
from core.config import *
import pygame
import time
pygame.init()


def fade_out_transition(screen, duration=1):
    delay = duration / 50
    s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    s = s.convert_alpha()
    s.fill((0,0,0))
    s.set_alpha(0)
    screen.blit(s, (0,0))
    for i in range(50):
        s.set_alpha(i)
        screen.blit(s, (0,0))
        pygame.display.update()
        time.sleep(delay)


def fade_in_transition(screen, render_function, duration=1):
    delay = duration / 255
    s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    s = s.convert_alpha()
    s.fill((0,0,0))
    s.set_alpha(255)
    screen.blit(s, (0,0))
    pygame.display.update()
    for i in range(255,0,-1):
        render_function()
        s.set_alpha(i)
        screen.blit(s, (0,0))
        pygame.display.update()
        time.sleep(delay)