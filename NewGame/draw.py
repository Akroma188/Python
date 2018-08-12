import pygame
#pylint: disable=E1101
pygame.init()

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 255)

# game display
disp_width = 800
disp_height = 600
gameDisplay = pygame.display.set_mode((disp_width, disp_height))

gameDisplay.fill(blue)

Pix = pygame.PixelArray(gameDisplay)

Pix[10][10] = green

# draw line
pygame.draw.line(gameDisplay, red, (200, 300), (500, 500), 5)

# draw circle 
pygame.draw.circle(gameDisplay, red, (50, 50), 50)

# draw rectangle
pygame.draw.rect(gameDisplay, green, (150, 150, 200, 100))

# draw polygon
pygame.draw.polygon(gameDisplay, white, ((140, 5), (200, 16), (88, 333)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.flip()
