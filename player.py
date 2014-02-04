import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):

	def __init__(self, x, y):
		self.x = x
		self.y = y
		
		#sprite
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load("img/human.gif").convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = [self.x, self.y]		
		
	def move(self, x,y, obstacles):
		old_x = self.x
		old_y = self.y
		
		self.rect.topleft = [old_x + x, old_y + y]
		
		collide = pygame.sprite.spritecollide(self, obstacles, False)
		if collide:
			print "boom"
			self.rect.topleft = [old_x, old_y]
			return 0
		else:
			self.x += x
			self.y += y
			return 1
			
	def update(self):
		pass