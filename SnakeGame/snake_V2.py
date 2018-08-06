import pygame
import time 
import random #for apple

pygame.init()

disp_width = 800
disp_height = 600
gameDisplay= pygame.display.set_mode((disp_width,disp_height))

pygame.display.set_caption('Snake_V2')

img = pygame.image.load('snake_head.png')

pygame.display.update()

white=(255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

clock = pygame.time.Clock()
direction = "right"
#font object
small_font = pygame.font.SysFont("comicsansms", 25) #size font 25
medium_font = pygame.font.SysFont("comicsansms", 50) #size font 25
large_font = pygame.font.SysFont("comicsansms", 80) #size font 25

def game_intro():
    intro = True
    while intro:
        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake 2.0", green, -100, "large")
        message_to_screen("Eat apple to improve your score", black, -30)
        message_to_screen("The more you eat the bigger you get", black, 10)
        message_to_screen("Enjoy yourself and try not to die!", black, 50)
        message_to_screen("Press C to play or Q to Quit", black, 180)
        pygame.display.update()
        clock.tick(15)

def snake(block_size, snake_list):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snake_list[-1][0], snake_list[-1][1]))

    for XnY in snake_list[:-1]: #everything except the last element -> the head
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def text_objects(text, color, size):
    if size == "small":
        textSurface = small_font.render(text, True, color)
    elif size == "medium":
        textSurface = medium_font.render(text, True, color)
    elif size == "large":
        textSurface = large_font.render(text, True, color)
    
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace = 0, size = "small"):
    texSurf, textRect = text_objects(msg, color, size)
    textRect.center = (disp_width/2), (disp_height/2) + y_displace
    gameDisplay.blit(texSurf, textRect)

def gameLoop():
    global direction 
    gameExit = False
    gameOver = False
    #Section for snake
    lead_x = 100
    lead_y = 100
    lead_change_x = 20
    lead_change_y = 0
    block_size = 20

    snake_list = []
    snake_length = 1

    randAppleX = round(random.randrange(0, disp_width - block_size)/10.0)*10.0
    randAppleY = round(random.randrange(0, disp_height - block_size)/10.0)*10.0

    velocity = 20
    FPS=15

    while not gameExit:
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game Over", red, -50, "large")
            message_to_screen("Press C to play again or Q to exit", black, 50, "medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False 
                    elif event.key == pygame.K_c:
                        gameLoop()
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = False
                gameExit = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_change_x = -velocity
                    lead_change_y = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_change_x = velocity
                    lead_change_y = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_change_y = -velocity
                    lead_change_x = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_change_y = velocity
                    lead_change_x = 0
                
        
        #Boundaries of walls
        if lead_x < 0 or lead_x >= disp_width or lead_y >= disp_height or lead_y < 0:
            gameOver = True
        #add position to snake
        lead_x += lead_change_x
        lead_y += lead_change_y 

        gameDisplay.fill((255,255,255)) 
        #draw apple
        apple_thickness = 30
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, apple_thickness, apple_thickness])

        #snake body
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head) #add element to the end of the list

        #delete first element (moving snake)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # check collisions with it self
        for segment in snake_list[:-1]:  #until the last element
            if segment == snake_head:
                gameOver = True

        snake(block_size, snake_list)
        pygame.display.update()

        #Eating the apple
        if lead_x > randAppleX and lead_x < randAppleX + apple_thickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + apple_thickness:
            if lead_y > randAppleY and lead_y < randAppleY + apple_thickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + apple_thickness:
                randAppleX = round(random.randrange(0, disp_width - block_size))#/10.0)*20.0
                randAppleY = round(random.randrange(0, disp_height - block_size))#/10.0)*20.0
                snake_length += 1

        clock.tick(FPS)

    gameDisplay.fill(white)
    message_to_screen("Game Over", red)
    pygame.display.update()
    time.sleep(1)
    pygame.quit()
    quit()

game_intro()
gameLoop()