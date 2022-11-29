# this file contains class for particles

import pygame
from pygame.math import Vector2
from random import randint

class Particles():
    def __init__(self):
        self.particles = []

    def load_particles(self, n, position=(250,250), velocity=(2,1), acceleration=(1,1), radius=10, color=(255, 255, 255)):
        for _ in range(n):
            self.particles.append(Particle(position, velocity, acceleration, radius, color))

    def splash(self, dt, screen):
        if self.particles:
            for particle in self.particles:
                particle.update(dt/10)
                particle.draw(screen)
                if particle.radius <= 0:
                    self.particles.remove(particle)
            return True
        else:
            return False

    def directional_flow(self, dt, screen, direction=None):
        if self.particles:
            for particle in self.particles:
                particle.direction = Vector2(direction)
                particle.update(dt/10)
                particle.draw(screen)
                if particle.radius <= 0:
                    #self.particles.append(Particle(particle.position,particle.velocity,particle.acceleration,particle.radius,particle.color))
                    self.particles.remove(particle)
            return True
        else:
            return False

class Particle():
    def __init__(self, position=(0,0), velocity=(1,1), acceleration=(1,1), radius=4, color=(255, 255, 255)):
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.acceleration = Vector2(acceleration)
        self.radius = radius
        self.color = color
        self.direction = None
    
    def update(self, dt):
        if self.direction is not None:
            direction_x = self.direction.x
            direction_y = self.direction.y
        else:
            direction_x = randint(1, 20) / 10
            direction_y = randint(1, 20) / 10 - 1
        self.radius -= dt
        self.position.x += direction_x * self.velocity.x * self.acceleration.x
        self.position.y += direction_y * self.velocity.y * self.acceleration.y

    def draw(self, screen, flags=pygame.BLEND_RGBA_ADD):
        circle = pygame.Surface((self.radius*2, self.radius*2))
        pygame.draw.circle(circle, self.color, (self.radius, self.radius), self.radius)
        circle.set_colorkey((0,0,0))
        screen.blit(circle, (self.position.x, self.position.y), special_flags=0)