
import pygame, sys
from pygame.locals import *
from level import *
from player import *

class Pyrou:
	def __init__(self):
		pygame.init()
		
		size = [800, 600]
		self.screen=pygame.display.set_mode(size)
		self.canvas = background = pygame.Surface([10000,10000])
		
		pygame.display.set_caption('Python rogue-like test') 
		
		#Sprite classes-groups.
		self.movables = pygame.sprite.Group()
		self.obstacles = pygame.sprite.Group()
		self.passables = pygame.sprite.Group()
		Player.groups = self.movables
		Obstacle.groups = self.obstacles
		Passable.groups = self.passables
		
		self.clock=pygame.time.Clock()
		
		self.map = Level(64,64)
	
		p_start = [self.map.start_x * 32,self.map.start_y * 32]	
		self.player = Player(p_start[0],p_start[1])
		self.camera_x = (size[0] / 2) - p_start[0]
		self.camera_y = (size[1] / 2) - p_start[1]
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit(0)
			
			self.update(event)
			self.draw()

	def draw(self):
		#draw stuff
		self.screen.fill((0,0,0))

		self.passables.draw(self.canvas)
		self.obstacles.draw(self.canvas)		
		self.movables.draw(self.canvas)
		
		#refresh screen
		self.clock.tick(20)
		self.screen.blit(self.canvas,(self.camera_x,self.camera_y))
		pygame.display.flip()

		
	def update(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT and self.player.move(-32,0, self.obstacles):
				self.camera_x += 32
			if event.key == pygame.K_RIGHT and self.player.move(32,0, self.obstacles):
				self.camera_x += -32
			if event.key == pygame.K_UP and self.player.move(0,-32, self.obstacles):
				self.camera_y += 32
			if event.key == pygame.K_DOWN and self.player.move(0,32, self.obstacles):
				self.camera_y += -32
			
			

if __name__ == "__main__" :
    game = Pyrou()
    game.run()