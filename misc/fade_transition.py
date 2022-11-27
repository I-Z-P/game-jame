# fade transition efect between two stages


import sys
sys.path.append('../')
from core.config import *
import pygame
import time
pygame.init()


def fade_transition(screen, duration=1):
    delay = duration / 100
    print(delay)
    s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    s = s.convert_alpha()
    s.fill((0,0,0))
    s.set_alpha(0)
    screen.blit(s, (0,0))
    for i in range(100):
        s.set_alpha(i)
        screen.blit(s, (0,0))
        pygame.display.update()
        time.sleep(delay)