import sys
sys.path.append('../')
from misc.animation import Animation
from particles.particles import Particles, Sparks
import pygame
from core.config import *
from core.render import debug_msg

from random import randint


class Stone():
	def __init__(self, color, images=stone):
		self.a = Animation(0)
		self.position = [200,250]
		self.a.load_player_body(images, type(images) is dict)
		self.sprite_group = pygame.sprite.Group()
		self.sprite_group.add(self.a)
		self.p = Particles()
		self.color = color
		self.sparking_position = [self.position[0]-self.a.rect.h/2, self.position[1]+self.a.rect.w/2]

	def load_particles(self):
		self.p.load_particles(3, position=self.position.copy(), color=self.color, velocity=[1,1], radius=0, max_radius=2, updating_value=-0.01)

	def update(self, screen):
		self.load_particles()
		self.a.animate(0.3, True, "full")
		self.a.update(self.position)
		self.p.splash(screen, flag=pygame.BLEND_RGBA_ADD)
		self.sprite_group.draw(screen)