# rendering objects on the screen


from config import DEV
import pygame

pygame.init()
font = pygame.font.Font(None, 30)


# display on screen debug info
def debug_msg(info, x = 10, y = 10):
    if DEV:
        display = pygame.display.get_surface()
        debug_surface = font.render(str(info), True, 'White')
        debug_rect = debug_surface.get_rect(topleft = (x,y))
        pygame.draw.rect(display, 'Black', debug_rect)
        display.blit(debug_surface, debug_rect)
    else:
        pass


# pin render functions here
def render(screen, player):
    screen.fill((49, 113, 181)) # background color
    player.render(screen)