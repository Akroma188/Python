import pygame
import random
import time
#pylint: disable=E1101

# Size of window -------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Size of each block - apple and snake 
BLOCK_SIZE = 20
FPS = 20

# Colors for the game --------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
yellow=(200, 200, 0)
light_yellow = (255, 255, 0)
RED = (255, 0, 0)
light_red = (255, 0, 0)
GREEN = (0, 155, 0)
light_green = (0, 255, 0)
BACKGROUND = (62, 62, 62)

# Initialize Window ---------------
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Snake')
clock = pygame.time.Clock()
snakeHead = pygame.image.load('head.png')
bodyPart = pygame.image.load('body.png')

# Fonts ---------------------------
small_font = pygame.font.SysFont('verdana', 25)  # size font 25
medium_font = pygame.font.SysFont('verdana', 50)  # size font 50
large_font = pygame.font.SysFont('verdana', 70)  # size font 70

class Apple:
	def __init__(self):
		self.apple_head_position = [round(random.randint(0, WINDOW_WIDTH - BLOCK_SIZE)/10.0)*20, 
								round(random.randint(0, WINDOW_HEIGHT - BLOCK_SIZE)/10.0)*20] 
		self.apple_on_game = True
	
	def spawn_apple(self):
		if self.apple_on_game == False:
			self.apple_head_position = [round(random.randint(0, WINDOW_WIDTH - BLOCK_SIZE)/10.0)*20, 
									round(random.randint(0, WINDOW_HEIGHT - BLOCK_SIZE)/10.0)*20]
			self.apple_on_game = True
			return self.apple_head_position

		

class Snake:
	def __init__(self):
		self.head_position = [400,300]
		self.body = [[380, 300], [360, 300], [340, 300]]
		self.direction = 'RIGHT'
		self.change_direction_to = self.direction
		self.score = 0

	def change_direction(self):
		if self.change_direction_to == 'RIGHT' and not self.direction == 'LEFT':
			self.direction = 'RIGHT'
		elif self.change_direction_to == 'LEFT' and not self.direction == 'RIGHT':
			self.direction = 'LEFT'
		elif self.change_direction_to == 'UP' and not self.direction == 'DOWN':
			self.direction = 'UP'
		elif self.change_direction_to == 'DOWN' and not self.direction == 'UP':
			self.direction = 'DOWN'
		
	def move(self):
		if self.direction == 'RIGHT':
			self.head_position[0] += BLOCK_SIZE
		elif self.direction == 'LEFT':
			self.head_position -= BLOCK_SIZE
		elif self.direction == 'UP':
			self.head_position -= BLOCK_SIZE
		elif self.direction == 'DOWN':
			self.head_position += BLOCK_SIZE

	def head_head_position(self):
		return self.head_position

	def full_body(self):
		return self.body

	def collision(self):
		if self.head_position[0] > WINDOW_WIDTH or self.head_position[0] < 0:
			return True
		elif self.head_position[1] > WINDOW_HEIGHT or self.head_position[1] < 0:
			return True

		for bodyPart in self.body:
			if self.head_position == bodyPart:
				return True
		return False

	def eaten_apple(self, apple_pos):
		if self.head_position == apple_pos:
			self.score += 1
			return True
		return False


# Functions to display Text ------------------------------------------
def text_objects(text, color, size):
	if size == 'small':
		textSurface = small_font.render(text, True, color)
	elif size == 'medium':
		textSurface = medium_font.render(text, True, color)
	elif size == 'large':
		textSurface = large_font.render(text, True, color)
	
	return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace = 0, size = 'small'):
	texSurf, textRect = text_objects(msg, color, size)
	textRect.center = (WINDOW_WIDTH/2), (WINDOW_HEIGHT/2) + y_displace
	screen.blit(texSurf, textRect)

# Funtions for Game Intro, Pause and Game Over -------------------------
def game_intro():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
				if event.key == pygame.K_q:
					pygame.quit()
					quit()

		screen.fill(BACKGROUND)
		message_to_screen('Welcome to Snake 2.0', GREEN, -100, 'large')
		message_to_screen('Eat apple to improve your score', WHITE, -30)
		message_to_screen('The more you eat the bigger you get', WHITE, 10)
		message_to_screen('Enjoy yourself and try not to die!', WHITE, 50)
		message_to_screen('Press C to play, P to Pause and Q to quit', WHITE, 180)
		pygame.display.flip()
		clock.tick(10)

def pause():
	paused = True
	#gameDisplay.fill(white)
	message_to_screen('Pause', WHITE, -100, 'large')
	message_to_screen('Press C to continue or Q to Quit', WHITE, 25, 'small')
	pygame.display.flip()
	clock.tick(5)
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

# Draw Snake ---------------------------------------------
def draw_snake(head, body, direction, head_img, body_img):
	if direction == "RIGHT":
		headPart = pygame.transform.rotate(head_img, 270)
	if direction == "LEFT":
		headPart = pygame.transform.rotate(head_img, 90)
	if direction == "UP":
		headPart = head_img
	if direction == "DOWN":
		headPart = pygame.transform.rotate(head_img, 180)

	screen.blit(headPart, (head[0], head[1]))  # make the head

	# Body 
	for pos in body:
		screen.blit(body_img, (pos[0], pos[1]))




# Game Definition
snake = Snake()
apple = Apple()

pygame.display.flip()

game_intro()
