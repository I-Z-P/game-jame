# this file contains class for particles

import pygame
from pygame.math import Vector2
from random import randint
from math import radians,cos,sin,pi


class Sparks():
    def __init__(self):
        self.sparks = []

    def load_sparks(self, n, position=[250,250], angle_range=[0, 360], speed=1, color=(255, 255, 255), scale=15):
        for _ in range(n):
            self.sparks.append(Spark(position, radians(randint(angle_range[0], angle_range[1])), speed, color, scale))

    def fire(self, dt, screen):
        if self.sparks:
            for i, spark in sorted(enumerate(self.sparks), reverse=True):
                spark.move(dt)
                spark.draw(screen)
                if not spark.alive:
                    self.sparks.pop(i)
        else:
            return False

class Spark():
    def __init__(self, loc, angle, speed, color, scale=1):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True

    def calculate_movement(self, dt):
        return [cos(self.angle) * self.speed * dt, sin(self.angle) * self.speed * dt]

    def move(self, dt):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]
        self.speed -= dt/30
        if self.speed <= 0:
            self.alive = False

    def draw(self, screen, offset=[0, 0]):
        if self.alive:
            points = [
                [self.loc[0] + cos(self.angle) * self.speed * self.scale, self.loc[1] + sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + cos(self.angle + pi / 2) * self.speed * self.scale * 0.3, self.loc[1] + sin(self.angle + pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - cos(self.angle) * self.speed * self.scale * 3.5, self.loc[1] - sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + cos(self.angle - pi / 2) * self.speed * self.scale * 0.3, self.loc[1] - sin(self.angle + pi / 2) * self.speed * self.scale * 0.3],
                ]
            self.draw_polygon(screen, points)

    def draw_polygon(self, screen, points, flag=0):
        # x_points = []
        # y_points = []
        # for point in points:
        #     x_points.append(point[0])
        #     y_points.append(point[1])
        # surf = pygame.Surface((max(x_points)-min(x_points), max(y_points)-min(y_points)))
        # pygame.draw.polygon(surf, self.color, points)
        # surf.set_colorkey((0,0,0))
        # screen.blit(surf, (0,0), special_flags=flag)
        pygame.draw.polygon(screen, self.color, points)

class Particles():
    def __init__(self):
        self.particles = []
        self.updating_value = 0.01
        self.flag = 0
        self.direction = [0,0]

    def load_particles(self, type=None, n=100, position=(250,250), velocity=(1,1), acceleration=(1,1), radius=5, color=(255, 255, 255), max_radius=10**4, min_radius=0, updating_value=0.1, flag=0, direction=[0,0]):
        n -= len(self.particles)
        self.flag = flag
        self.updating_value = updating_value
        self.direction = direction
        for _ in range(n):
            self.particles.append(Particle(position, velocity, acceleration, radius, color, min_radius, max_radius))

    def splash(self, screen, flag=0):
        if self.particles:
            for particle in self.particles:
                particle.update(self.updating_value, self.direction, [20, 20])
                particle.draw(screen, flag=self.flag)
                if not particle.alive:
                    self.particles.remove(particle)
            return True
        else:
            return False

class Particle():
    def __init__(self, position=(0,0), velocity=(1,1), acceleration=(1,1), radius=4, color=(255, 255, 255), min_radius=0, max_radius=10**4, gravity=5):
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.acceleration = Vector2(acceleration)
        self.radius = radius
        self.color = color
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.gravity = gravity
        self.vertical_momentum = 0
        self.alive = True
    
    def update(self, dt, direction, range):
        self.vertical_momentum += dt/(self.gravity*5)
        if self.vertical_momentum > self.gravity:
            self.vertical_momentum = self.gravity
        direction_x = randint(1, 20) / 10 + float(direction[0]) - 1
        direction_y = randint(1, 20) / 10 + float(direction[1]) - 1 + self.vertical_momentum
        self.radius -= dt
        if self.radius < self.min_radius or self.radius > self.max_radius:
            self.alive = False
        self.position.x += direction_x * self.velocity.x * self.acceleration.x
        self.position.y += direction_y * self.velocity.y * self.acceleration.y

    def draw(self, screen, flag=0):
        circle = pygame.Surface((self.radius*2, self.radius*2))
        pygame.draw.circle(circle, self.color, (self.radius, self.radius), self.radius)
        circle.set_colorkey((0,0,0))
        screen.blit(circle, (self.position.x, self.position.y), special_flags=flag)

    def get_position(self):
        return [self.position.x, self.position.y]