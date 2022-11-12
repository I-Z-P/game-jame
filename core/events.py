# handling keyboard events and calling the corresponding functions


import pygame


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
            pygame.quit()
        # keys = pygame.key.get_pressed()