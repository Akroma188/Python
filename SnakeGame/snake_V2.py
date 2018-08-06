import pygame
import time 
import random #for apple

pygame.init()

disp_width = 800
disp_height = 600
gameDisplay= pygame.display.set_mode((disp_width,disp_height))

pygame.display.set_caption('Snake_V2')

pygame.display.update()

white=(255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

clock = pygame.time.Clock()

#font object
font = pygame.font.SysFont(None, 25) #size font 25

def snake(block_size, snake_list):
    for XnY in snake_list:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def game_over_msg(msg, color):
    gameDisplay.fill(white)
    screen_text = font.render(msg, True, color) #True for anti-aliasing
    gameDisplay.blit(screen_text, [disp_width/2, disp_height/2])

def gameLoop():
    gameExit = False
    gameOver = False
    #Section for snake
    lead_x = 100
    lead_y = 100
    lead_change_x = 0
    lead_change_y = 0
    block_size = 10

    snake_list = []
    snake_length = 1

    randAppleX = round(random.randrange(0, disp_width - block_size)/10.0)*10.0
    randAppleY = round(random.randrange(0, disp_height - block_size)/10.0)*10.0

    velocity = 10
    FPS=24

    while not gameExit:
        while gameOver == True:
            gameDisplay.fill(white)
            game_over_msg("Game Over, Press C to play again or Q to exit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                        break
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
                    lead_change_x = -velocity
                    lead_change_y = 0
                elif event.key == pygame.K_RIGHT:
                    lead_change_x = velocity
                    lead_change_y = 0
                elif event.key == pygame.K_UP:
                    lead_change_y = -velocity
                    lead_change_x = 0
                elif event.key == pygame.K_DOWN:
                    lead_change_y = velocity
                    lead_change_x = 0
                
        
        #Boundaries
        if lead_x < 0 or lead_x >= disp_width or lead_y >= disp_height or lead_y < 0:
            gameOver = True

        lead_x += lead_change_x
        lead_y += lead_change_y 

        gameDisplay.fill((255,255,255)) 
        #draw apple
        apple_thickness = 30
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, apple_thickness, apple_thickness])

        
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

        if lead_x > randAppleX and lead_x < randAppleX + apple_thickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + apple_thickness:
            if lead_y > randAppleY and lead_y < randAppleY + apple_thickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + apple_thickness:
                randAppleX = round(random.randrange(0, disp_width - block_size))#/10.0)*10.0
                randAppleY = round(random.randrange(0, disp_height - block_size))#/10.0)*10.0
                snake_length += 1

        clock.tick(FPS)

    game_over_msg("Game Over", red)
    pygame.display.update()
    time.sleep(1)
    pygame.quit()
    quit()

gameLoop()