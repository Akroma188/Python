import pygame
import time 
import random #for apple

pygame.init()

disp_width = 800
disp_height = 600
gameDisplay= pygame.display.set_mode((disp_width,disp_height))

pygame.display.set_caption('Snake_V2')

img = pygame.image.load('snake_head.png')
apple_img = pygame.image.load("apple.png")

icon = pygame.image.load("icon_30.png")
pygame.display.set_icon(icon)

pygame.display.update()

white=(255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

clock = pygame.time.Clock()
direction = "right"
block_size = 20
FPS=20
#font object
small_font = pygame.font.SysFont("comicsansms", 25) #size font 25
medium_font = pygame.font.SysFont("comicsansms", 50) #size font 25
large_font = pygame.font.SysFont("comicsansms", 70) #size font 25

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


        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake 2.0", green, -100, "large")
        message_to_screen("Eat apple to improve your score", black, -30)
        message_to_screen("The more you eat the bigger you get", black, 10)
        message_to_screen("Enjoy yourself and try not to die!", black, 50)
        message_to_screen("Press C to play, P to Pause and Q to quit", black, 180)
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

    gameDisplay.blit(head, (snake_list[-1][0], snake_list[-1][1]))  #make the head

    for XnY in snake_list[:-1]: #everything except the last element -> the head
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def randAppleGen():
    randAppleX = round(random.randrange(0, disp_width - block_size)/10.0)*20.0
    randAppleY = round(random.randrange(0, disp_height - block_size)/10.0)*20.0
    return randAppleX, randAppleY

def score(score):
    text = small_font.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])

def pause():
    paused = True
    #gameDisplay.fill(white)
    message_to_screen("Pause", black, -100, "large")
    message_to_screen("Press C to continue or Q to Quit", black, 25, "small")
    pygame.display.update()
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
    direction = "right"
    gameExit = False
    gameOver = False
    velocity = 20
    #Section for snake
    lead_x = 100
    lead_y = 100
    lead_change_x = 20
    lead_change_y = 0
    

    snake_list = []
    snake_length = 1
    randAppleX=3000
    randAppleY=3000
    apple_thickness = 20

    while randAppleX > disp_width- apple_thickness or randAppleY > disp_height - apple_thickness:
        randAppleX, randAppleY = randAppleGen()


    while not gameExit:
        if gameOver == True:
            #gameDisplay.fill(white)
            message_to_screen("Game Over", red, -50, "large")
            message_to_screen("Press C to play again or Q to exit", black, 50, "medium")
            pygame.display.update()
        while gameOver == True:
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
                elif event.key == pygame.K_p:
                    pause()
                
        
        #Boundaries of walls
        if lead_x < 0 or lead_x >= disp_width or lead_y >= disp_height or lead_y < 0:
            gameOver = True
        #add position to snake
        lead_x += lead_change_x
        lead_y += lead_change_y 

        gameDisplay.fill((255,255,255)) 

        #draw apple
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, apple_thickness, apple_thickness])
        gameDisplay.blit(apple_img, (randAppleX, randAppleY))

        #snake body
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)   #lead is the head
        snake_list.append(snake_head) #add element to the end of the list

        #delete first element (moving snake)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # check collisions with it self
        for segment in snake_list[:-1]:  #until the last element
            if segment == snake_head:
                gameOver = True

        snake(block_size, snake_list)
        score(snake_length-1)
        pygame.display.update()

        #Eating the apple
        if lead_x > randAppleX and lead_x < randAppleX + apple_thickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + apple_thickness or lead_x == randAppleX:
            if lead_y > randAppleY and lead_y < randAppleY + apple_thickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + apple_thickness or lead_y == randAppleY:
                randAppleX, randAppleY = randAppleGen()
                while randAppleX > disp_width- apple_thickness or randAppleY > disp_height - apple_thickness:
                    randAppleX, randAppleY = randAppleGen()
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