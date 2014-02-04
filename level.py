import pygame, random, math, itertools
from pygame.locals import *

class Tile(pygame.sprite.Sprite):

	def __init__(self, img_file, pos_x, pos_y):
		
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load(img_file).convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = [pos_x, pos_y]	
	
class Obstacle(Tile):
	pass

class Passable(Tile):
	pass

class Level:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		
		#Store for sprite objects
		self.tiles = []
		
		#Divide the grid into larger cells
		cell_x = x / 10
		cell_y = y / 10
		
		### Create empty grid
		self.grid = [[] for i in range(y)]
		for i in range(y):
			self.grid[i] = [-1] * x
		
		r_min = 6
		r_max = 10
		rooms = []
		

		### Place rooms randomly in cells
		for i in range(cell_x):
			for j in range(cell_y):
			
				if random.random() > 0.5:
					x1 = i * 8
					y1 = j * 8
					x2 = x1 + random.randrange(r_min, r_max)
					y2 = y1 + random.randrange(r_min, r_max)
					
					rooms.append([x1, y1, x2, y2])
		
		"""
		### Place cells uniformly
		num_rooms = int( ((self.x * self.y )  / (r_max ** 2)) * 0.6 )
		for i in range(num_rooms):
		
			x1 = random.randrange(1, self.x - r_max - 1)
			y1 = random.randrange(1, self.y - r_max - 1)
			x2 = x1 + random.randrange(r_min, r_max)
			y2 = y1 + random.randrange(r_min, r_max)
			
			rooms.append([x1, y1, x2, y2])		
		"""
		
		### length array, all to all rooms
		lengths = [[] for i in range(len(rooms))]
		for i in range(len(rooms)):
			lengths[i] = [0] * len(rooms)
		
		ii = 0	
		for i in rooms:
			ij = 0
			for j in rooms:
				lengths[ii][ij] = math.sqrt( (i[0]-j[0])**2 + (i[1]-j[1])**2 )
				ij += 1
			ii += 1		
			
			
		### Find MST / Prims algo
		Vnew = [] 
		Enew = [] #edges as [i,j] pairs | i,j are indices in rooms list
		
		start_room = random.choice(range(len(rooms)))
		Vnew.append(start_room)
		
		#set player start
		self.start_x = int((rooms[start_room][0] + rooms[start_room][2]) / 2)
		self.start_y = int((rooms[start_room][1] + rooms[start_room][3]) / 2)
		
		while len(Vnew) < len(rooms):
			
			e_min = max(sum(lengths, [])) + 1
			for i in Vnew:
				i_len = lengths[i]
				for j in range(len(i_len)):
					if i_len[j] < e_min and Vnew.count(j) == 0:
						e_min = i_len[j]; min_j = j; min_i = i

			Vnew.append(min_j)
			Enew.append([min_i, min_j])
			
		### Room creation
		for room in rooms:
		
			#Floors in the middle
			for i in range(room[1], room[3]):
				for j in range(room[0], room[2]):
					self.grid[i][j] = 0
			
			#Walls around
			for i in range(room[1], room[3]):
				self.grid[i][room[0]] = 1
				self.grid[i][room[2]] = 1
			
			for i in range(room[0], room[2]):
				self.grid[room[1]][i] = 1
				self.grid[room[3]][i] = 1
			self.grid[room[3]][room[2]] = 1
				
		
		### Create tunnels
		for i in Enew:
			src = i[0]; dst = i[1]
			src_piv = [(rooms[src][0] + rooms[src][2])/2, (rooms[src][1] + rooms[src][3])/2]
			dst_piv = [(rooms[dst][0] + rooms[dst][2])/2, (rooms[dst][1] + rooms[dst][3])/2]

			mid_x = int(math.fabs((src_piv[0] + dst_piv[0]) / 2))
			mid_y = int(math.fabs((src_piv[1] + dst_piv[1]) / 2))
				

			#if (mid_x-mid_y) >= (mid_y-mid_x):
			#self.tunnel(src_piv, [mid_x, src_piv[1]])
			#self.tunnel([mid_x, src_piv[1]], [mid_x, dst_piv[1]])
			#self.tunnel([mid_x, dst_piv[1]], dst_piv)
			#else:
			self.tunnel(src_piv, [src_piv[0], mid_y], 0)
			self.tunnel([dst_piv[0], mid_y] ,dst_piv, 0)
			self.tunnel([src_piv[0], mid_y], [dst_piv[0], mid_y], 3)

			
		### To sprite objects
		for i in range(y):
			for j in range(x):
				if self.grid[i][j] == 0:
					self.tiles.append(Passable("img/floor.png", j * 32, i * 32))
				elif self.grid[i][j] == 1:
					self.tiles.append(Obstacle("img/wall.png", j * 32, i * 32))
				elif self.grid[i][j] == 3:
					self.tiles.append(Passable("img/conn.png", j * 32, i * 32))

		
	def tunnel(self, src, dst, tile):
	
		x_range = range(min(src[0], dst[0]), max(src[0], dst[0]))
		y_range = range(min(src[1], dst[1]), max(src[1], dst[1]))
		
		if len(x_range) == 0:
			x_range = [src[0]]
		elif len(y_range) == 0:
			y_range = [src[1]]
		
		for x in x_range:
			for y in y_range:
				self.grid[y][x] = tile
				
				for x2 in range(x-1, x+2):
					for y2 in range(y-1, y+2):
						if self.grid[y2][x2] == -1:
							self.grid[y2][x2] = 1
				
			
		
		