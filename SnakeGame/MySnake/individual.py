import pygame 
import random
import numpy as np
import neuralNetwork as neural


BLOCK_SIZE = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
class Snake:
    
	def __init__(self):
		self.head_position = [380,300]
		self.body = [[380, 300], [360, 300], [340, 300]]
		self.direction = 'RIGHT'
		self.score = 0
		self.fitness = 0
		self.clock = pygame.time.Clock()
		self.time = 0
		self.apple_position = 0
		self.apple_on_game = False
		self.brain = neural.NeuralNetwork(24, 18, 18, 4)
		self.brain.create_weight_matrices()
		
	def spawn_apple(self):
		if self.apple_on_game == False:
			self.apple_position = [random.randint(0,(WINDOW_WIDTH-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE, 
									random.randint(0,(WINDOW_HEIGHT-BLOCK_SIZE)/BLOCK_SIZE) * BLOCK_SIZE]
			self.apple_on_game = True
			return self.apple_position

	def change_direction(self, dir):
		if dir == 'RIGHT' and not self.direction == 'LEFT':
			self.direction = 'RIGHT'
		elif dir == 'LEFT' and not self.direction == 'RIGHT':
			self.direction = 'LEFT'
		elif dir == 'UP' and not self.direction == 'DOWN':
			self.direction = 'UP'
		elif dir == 'DOWN' and not self.direction == 'UP':
			self.direction = 'DOWN'
		
	def move(self):
		if self.direction == 'RIGHT':
			self.head_position[0] += BLOCK_SIZE
		elif self.direction == 'LEFT':
			self.head_position[0] -= BLOCK_SIZE
		elif self.direction == 'UP':
			self.head_position[1] -= BLOCK_SIZE
		elif self.direction == 'DOWN':
			self.head_position[1] += BLOCK_SIZE

		self.body.insert(0, list(self.head_position))
		if self.head_position != self.apple_position:
			self.body.pop() 

	def collision(self):
		if self.head_position[0] >= WINDOW_WIDTH or self.head_position[0] < 0:
			return True
		elif self.head_position[1] >= WINDOW_HEIGHT or self.head_position[1] < 0:
			print(self.head_position[0], self.head_position[1])
			return True

		for bodyPart in self.body[1:]:
			if self.head_position == bodyPart:
				return True
		return False

	def eaten_apple(self):
		if self.head_position == self.apple_position:
			self.score += 1
			return True
		return False

	def make_a_clock(self):
		self.clock = pygame.time.Clock()

	def get_time_alive(self):
		self.clock.tick()
		dt = self.clock.get_time()
		self.time += dt
		return self.time

	def calcFitness(self):
		if self.score < 10:
			self.fitness = (self.time/1000) ** 2 + self.score **2
		else:
			self.fitness = (self.time/1000) * self.score ** 2
		return round(self.fitness, 2)

	# vision looks up in 8 directions
	# takes in account, distance to apple, wall and body
	# 8
	def eyes(self):
		vision=[]
		# Up direction 
		result = self.look_direction(vector = [0, -BLOCK_SIZE])
		vision.append(result[0])
		vision.append(result[1])
		vision.append(result[2])

		# UP/RIGHT direction
		result = self.look_direction(vector = [BLOCK_SIZE, -BLOCK_SIZE])
		vision.append(result[0])
		vision.append(result[1])
		vision.append(result[2])

		# UP/LEFT direction
		result = self.look_direction(vector = [-BLOCK_SIZE, -BLOCK_SIZE])
		vision.append(result[0])
		vision.append(result[1])
		vision.append(result[2])

		# RIGHT direction
		result = self.look_direction(vector = [BLOCK_SIZE, 0])
		vision.append(result[0])
		vision.append(result[1])
		vision.append(result[2])

		# LEFT direction
		result = self.look_direction(vector = [-BLOCK_SIZE, 0])
		vision.append(result[0])
		vision.append(result[1])
		vision.append(result[2])

		# DOWN direction
		result = self.look_direction(vector = [0, BLOCK_SIZE])
		vision.append(result[0])
		vision.append(result[1])
		vision.append(result[2])

		# DOWN/RIGHTdirection
		result = self.look_direction(vector = [BLOCK_SIZE, BLOCK_SIZE])
		vision.append(result[0])
		vision.append(result[1])
		vision.append(result[2])

		# DOWN/LEFT direction
		result = self.look_direction(vector = [-BLOCK_SIZE, BLOCK_SIZE])
		vision.append(result[0])
		vision.append(result[1])
		vision.append(result[2])

		
		return vision

	def look_direction(self, vector=[0,0]):
		result=[]
		# make list to matrix using numpy
		vector = np.array(vector)
		actual_pos = np.array(self.head_position)
		applePos = np.array(self.apple_position)

		appleFound = False
		bodyFound = False
		# (actual_pos[0] > 0) or (actual_pos[0] < WINDOW_WIDTH) or (actual_pos[1] > 0) or (actual_pos[1] < WINDOW_HEIGHT):
		while actual_pos[0] > 0 and actual_pos[0] < WINDOW_WIDTH and actual_pos[1] > 0 and actual_pos[1] < WINDOW_HEIGHT:
			actual_pos += vector
			if not appleFound:
				if np.array_equal(actual_pos, applePos):
					head_pos=np.array(self.head_position)
					norm_position = actual_pos-head_pos
					distance = np.sqrt(norm_position[0]**2 + norm_position[1]**2)/10
					if distance == 0:
							distance = 1
					result.insert(0, np.round(1/distance, 4))
					print('Apple FOUND !!!!')
					appleFound = True

			if not bodyFound:
				for bodyPart in self.body[1:]:
					actualPos = list(actual_pos) # if statements for numpy are bad..
					if actualPos == bodyPart:
						head_pos=np.array(self.head_position)
						norm_position = actual_pos-head_pos
						distance = np.sqrt(norm_position[0]**2 + norm_position[1]**2)/10
						if distance == 0:
							distance = 1
						result.insert(1, np.round(1/distance, 4))
						bodyFound = True
		
		if not bodyFound:
			result.insert(1, False)
		if not appleFound:
			result.insert(0, False)

		head_pos=np.array(self.head_position)
		norm_position = actual_pos-head_pos
		distance = np.sqrt(norm_position[0]**2 + norm_position[1]**2)/10
		if distance == 0:
			distance = 1
		result.insert(2, np.round(1/distance, 4))

		return list(result)

	def decide_where_to_move(self):
		information = self.eyes()

		result = self.brain.output(information)
		print(result)

		index = result.index(max(result))
		print(index)

		if index == 0:
			self.change_direction('UP')
		if index == 1:
			self.change_direction('DOWN')
		if index == 2:
			self.change_direction('RIGHT')
		if index == 3:
			self.change_direction('LEFT')

