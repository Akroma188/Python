import pygame
import time

pygame.init()

disp_width = 800
disp_height = 600
gameDisplay= pygame.display.set_mode((disp_width,disp_height))

pygame.display.set_caption('SLither')

pygame.display.update()

white=(255,255,255)
black = (0,0,0)
red = (255,0,0)

clock = pygame.time.Clock()

#font object
font = pygame.font.SysFont(None, 25) #size font 25

def message_to_screen(msg, color):
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

    velocity = 10
    body_width = 10
    body_height = 10

    FPS=30

    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game Over, Press C to play again or Q to exit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
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
                
        lead_x += lead_change_x
        lead_y += lead_change_y
        #Boundaries
        if lead_x < 0 or lead_x >= disp_width or lead_y >= disp_height or lead_y < 0:
            gameOver = True

        gameDisplay.fill((255,255,255)) 
        pygame.draw.rect(gameDisplay, black, [lead_x, lead_y, body_width, body_height])

        pygame.display.update()

        clock.tick(FPS)

    message_to_screen("Game Over", red)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()

gameLoop()