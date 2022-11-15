# handling keyboard events and calling the corresponding functions


import pygame
from config import DEV


def keyboard_assignments(event):
    if DEV: print('Pressed key in ascii:', event.key) 
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        pygame.quit()


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            keyboard_assignments(event)