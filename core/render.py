# rendering objects on the screen


from config import *
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


class Fps_counter():
    def __init__(self, screen):
        self.screen = screen
        self.run = FPS_COUNTER
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.debug_surface = font.render(str(self.fps), True, 'White')
        self.debug_rect = self.debug_surface.get_rect(topleft = (WINDOW_WIDTH-60,20))

    def update(self):
        self.fps = self.clock.get_fps()
        self.render()

    def render(self):
        self.debug_surface = font.render(str(self.fps), True, 'White')
        self.debug_rect = self.debug_surface.get_rect(topleft = (WINDOW_WIDTH-60,20))
        pygame.draw.rect(self.screen, 'Black', self.debug_rect)
        self.screen.blit(self.debug_surface, self.debug_rect)


# pin render functions here
def render(screen, player, level, camera, fps_counter):
    screen.fill((49, 113, 181)) # background color
    level.render(screen, camera)
    player.render(screen)
    if fps_counter.run:
        fps_counter.update()