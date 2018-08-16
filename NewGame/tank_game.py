import pygame
import time 
import random  # for apple
#pylint: disable=E1101
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

yellow=(200, 200, 0)
light_yellow = (255, 255, 0)

red = (200, 0, 0)
light_red = (255, 0, 0)

green = (34, 177, 76)
light_green = (0, 255, 0)

disp_width = 800
disp_height = 600
gameDisplay = pygame.display.set_mode((disp_width, disp_height))

pygame.display.set_caption('Tanks')

# img = pygame.image.load('snake_head.png')
# apple_img = pygame.image.load("apple.png")

# icon = pygame.image.load("icon_30.png")
# pygame.display.set_icon(icon)

pygame.display.update()

clock = pygame.time.Clock()

# tank cts
tankWidth = 40
tankHeight = 20
turretWidth = 5
wheelWidth = 5

ground_height = 35

# font object
small_font = pygame.font.SysFont("comicsansms", 25)  # size font 25
medium_font = pygame.font.SysFont("comicsansms", 50)  # size font 25
large_font = pygame.font.SysFont("comicsansms", 70)  # size font 25

def tank(x, y, turrPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x-27, y-2),
                        (x-26, y-5),
                        (x-25, y-8),
                        (x-23, y-12),
                        (x-20, y-14),
                        (x-18, y-15),
                        (x-15, y-17),
                        (x-13, y-19),
                        (x-11, y-21)]

    pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))

    # draw gun
    pygame.draw.line(gameDisplay, black, (x, y), possibleTurrets[turrPos], turretWidth)
    starX = 15
    for num in range(7):
        pygame.draw.circle(gameDisplay, black, (x-starX, y+20), wheelWidth)
        starX -= 5

    return possibleTurrets[turrPos]


def enemy_tank(x, y, turrPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x+27, y-2),
                        (x+26, y-5),
                        (x+25, y-8),
                        (x+23, y-12),
                        (x+20, y-14),
                        (x+18, y-15),
                        (x+15, y-17),
                        (x+13, y-19),
                        (x+11, y-21)]

    pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))

    # draw gun
    pygame.draw.line(gameDisplay, black, (x, y), possibleTurrets[turrPos], turretWidth)
    startX = 15
    for num in range(7):
        pygame.draw.circle(gameDisplay, black, (x-startX, y+20), wheelWidth)
        startX -= 5

    return possibleTurrets[turrPos]

def barrier(x_barrier_location, random_height, barrier_width):
    
    pygame.draw.rect(gameDisplay, black, [x_barrier_location, disp_height - random_height, barrier_width, random_height])

def explosion(x, y, size):
    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        start_point = x,y
        color_choices = [red, light_red, yellow, light_yellow]

        magnitude = 1
        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1 * magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-1 * magnitude, magnitude)

            pygame.draw.circle(gameDisplay, color_choices[random.randrange(0, 4)], (exploding_bit_x, exploding_bit_y), random.randrange(1, 5))
            magnitude += 1

            pygame.display.update()

            clock.tick(100)

        explode = False

def fireShell(xy, tankx, tanky, turPos, gun_power, x_barrier_location, barrier_width, random_height, enemy_tankX, enemy_tankY):
    damage = 0
    fire = True
    starting_shell = list(xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        pygame.draw.circle(gameDisplay, red, (starting_shell[0], starting_shell[1]), 5)

        starting_shell[0] -= (12 - turPos) * 2

        starting_shell[1] += int((((starting_shell[0] - xy[0]) * 0.015/(gun_power/50)) ** 2) - (turPos+turPos/(12 - turPos)))

        if starting_shell[1] > disp_height - ground_height:
            fire = False
            hit_x = int((starting_shell[0] * (disp_height - ground_height))/starting_shell[1])
            hit_y = int(disp_height - ground_height)
            if enemy_tankX + 15 > hit_x > enemy_tankX - 15:
                damage = 25
            explosion(hit_x, hit_y, 50)

        check_x_1 = starting_shell[0] <= x_barrier_location + barrier_width
        check_x_2 = starting_shell[0] >= x_barrier_location
        check_y_1 = starting_shell[1] <= disp_height
        check_y_2 = starting_shell[1] >= disp_height - random_height

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            fire = False
            hit_x = int(starting_shell[0])
            hit_y = int(starting_shell[1])
            explosion(hit_x, hit_y, 50)

        pygame.display.update()
        clock.tick(100)
    return damage

def e_fireShell(xy, tankx, tanky, turPos, gun_power, x_barrier_location, barrier_width, random_height, pTankX, pTankY):
    damage = 0
    curr_power = 1
    power_found = False

    while not power_found:
        curr_power +=1
        if curr_power > 100:
            power_found = True
        fire = True
        starting_shell = list(xy)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            starting_shell[0] += (12 - turPos) * 2

            starting_shell[1] += int((((starting_shell[0] - xy[0]) * 0.015/(curr_power/50)) ** 2) - (turPos+turPos/(12 - turPos)))

            if starting_shell[1] > disp_height - ground_height:
                hit_x = int((starting_shell[0] * (disp_height - ground_height))/starting_shell[1])
                hit_y = int(disp_height - ground_height)
                if pTankX + 15 > hit_x > pTankX - 15:
                    power_found = True
                fire = False

            check_x_1 = starting_shell[0] <= x_barrier_location + barrier_width
            check_x_2 = starting_shell[0] >= x_barrier_location
            check_y_1 = starting_shell[1] <= disp_height
            check_y_2 = starting_shell[1] >= disp_height - random_height

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int(starting_shell[0])
                hit_y = int(starting_shell[1])
                fire = False

    fire = True
    starting_shell = list(xy)
    
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        pygame.draw.circle(gameDisplay, red, (starting_shell[0], starting_shell[1]), 5)

        starting_shell[0] += (12 - turPos) * 2

        starting_shell[1] += int((((starting_shell[0] - xy[0]) * 0.015/(curr_power/50)) ** 2) - (turPos+turPos/(12 - turPos)))

        if starting_shell[1] > disp_height - ground_height:
            hit_x = int((starting_shell[0] * (disp_height - ground_height))/starting_shell[1])
            hit_y = int(disp_height - ground_height)
            if pTankX + 15 > hit_x > pTankX - 15:
                print('Hit target')
                damage = 25
            explosion(hit_x, hit_y, 50)
            fire = False

        check_x_1 = starting_shell[0] <= x_barrier_location + barrier_width
        check_x_2 = starting_shell[0] >= x_barrier_location
        check_y_1 = starting_shell[1] <= disp_height
        check_y_2 = starting_shell[1] >= disp_height - random_height

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int(starting_shell[0])
            hit_y = int(starting_shell[1])
            explosion(hit_x, hit_y, 50)
            fire = False

        pygame.display.update()
        clock.tick(100)

    return damage

def power(level):
    text = small_font.render("Power: " + str(level) + "%", True, black)
    gameDisplay.blit(text, [disp_height/2, 0])

def health_bar(player_health, enemy_health):
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red

    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red

    pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))
    pygame.draw.rect(gameDisplay, enemy_health_color, (20, 25, enemy_health, 25))

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
        message_to_screen("Welcome to Tanks!", green, -100, "large")
        message_to_screen("Shoot and destroy", black, -30)
        message_to_screen("The more you destroy the harder it gets", black, 10)
        message_to_screen("Enjoy yourself and try not to die!", black, 50)
        # message_to_screen("Press C to play, P to Pause and Q to quit", black, 180)

        button("Play", 150, 500, 100, 50, green, light_green, action = 'play')
        button("Controls", 350, 500, 100, 50, yellow, light_yellow, action = 'controls')
        button("Quit", 550, 500, 100, 50, red, light_red, action = 'quit')

        pygame.display.update()
        clock.tick(15)

def game_over():
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen("Game over", green, -100, "large")
        message_to_screen("You die", black, -30)
        # message_to_screen("Press C to play, P to Pause and Q to quit", black, 180)

        button("Play Again", 150, 500, 150, 50, green, light_green, action = 'play')
        button("Controls", 350, 500, 100, 50, yellow, light_yellow, action = 'controls')
        button("Quit", 550, 500, 100, 50, red, light_red, action = 'quit')

        pygame.display.update()
        clock.tick(15)

def you_win():
    wine = True
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen("You Won", green, -100, "large")
        message_to_screen("Congratulations", black, -30)
        # message_to_screen("Press C to play, P to Pause and Q to quit", black, 180)

        button("Play Again", 150, 500, 150, 50, green, light_green, action = 'play')
        button("Controls", 350, 500, 100, 50, yellow, light_yellow, action = 'controls')
        button("Quit", 550, 500, 100, 50, red, light_red, action = 'quit')

        pygame.display.update()
        clock.tick(15)

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

def text_to_button(msg, color, button_x, button_y, button_w, button_h, size='small'):
    texSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((button_x + (button_w/2)), button_y + (button_h/2))
    gameDisplay.blit(texSurf, textRect)

def game_controls():
    gcontrol = True
    while gcontrol:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen("Controls", green, -100, "large")
        message_to_screen("Fire: Space Bar", black, -30)
        message_to_screen("Move Turret: Up and Down Arrows", black, 10)
        message_to_screen("Move Tank: Right and Left Arrows", black, 50)
        message_to_screen("Pause: P", black, 90)
        # message_to_screen("Press C to play, P to Pause and Q to quit", black, 180)

        button("Play", 150, 500, 100, 50, green, light_green, action = 'play')
        button("Menu", 350, 500, 100, 50, yellow, light_yellow, action = 'menu')
        button("Quit", 550, 500, 100, 50, red, light_red, action = 'quit')

        pygame.display.update()
        clock.tick(15)

def button(msg, x, y, width, height, inactive_color, active_color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y, width, height))
        if click [0] == 1 and action != None:
            if action == 'quit':
                pygame.quit()
            elif action == 'controls':
                game_controls()
            elif action == 'play':
                gameLoop()
            elif action == 'menu':
                game_intro()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y, width, height))

    text_to_button(msg, black, x, y, width, height)


def message_to_screen(msg, color, y_displace = 0, size = "small"):
    texSurf, textRect = text_objects(msg, color, size)
    textRect.center = (disp_width/2), (disp_height/2) + y_displace
    gameDisplay.blit(texSurf, textRect)




def gameLoop():

    gameExit = False
    gameOver = False
    FPS = 20

    barrier_width = 50

    # our tank
    mainTankX = disp_width * 0.9
    mainTankY = disp_height * 0.9
    tankMove = 0
    currTurPos = 0
    changeTur = 0
    player_health = 100

    # enemy tank
    enemyTankX = disp_width * 0.1
    enemyTankY = disp_height * 0.9
    enemy_health = 100

    fire_power = 50
    power_change = 0

    x_barrier_location = disp_width/2 + random.randint(-0.2 * disp_width, 0.2 * disp_width)
    random_height = random.randrange(disp_height * 0.1, disp_height * 0.6)

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
                    tankMove = -5
                elif event.key == pygame.K_RIGHT:
                    tankMove = 5
                elif event.key == pygame.K_UP:
                    changeTur = 1
                elif event.key == pygame.K_DOWN:
                    changeTur = -1
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_SPACE:
                    damage = fireShell(gun, mainTankX, mainTankY, currTurPos, fire_power, x_barrier_location, barrier_width, random_height, enemyTankX, enemyTankY)
                    enemy_health -= damage
                    damage = e_fireShell(enemy_gun, enemyTankX, enemyTankY, 8, 50, x_barrier_location, barrier_width, random_height, mainTankX, mainTankY)
                    player_health -= damage
                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0
        

        mainTankX += tankMove
        currTurPos += changeTur
        if currTurPos > 8:
            currTurPos = 8
        elif currTurPos < 0:
            currTurPos = 0

        if mainTankX - tankWidth/2 < x_barrier_location + barrier_width:
            mainTankX += 5


        gameDisplay.fill(white)
        health_bar(player_health, enemy_health)
        gun = tank(mainTankX, mainTankY, currTurPos)

        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)

        fire_power += power_change
        power(fire_power)
        
        barrier(x_barrier_location, random_height, barrier_width)
        gameDisplay.fill(green, rect=[0, disp_height - ground_height, disp_width, ground_height])
        pygame.display.update()

        if player_health < 1:
            game_over()
        elif enemy_health <1:
            you_win()

        clock.tick(FPS)

    gameDisplay.fill(white)
    message_to_screen("Game Over", red)
    pygame.display.update()
    time.sleep(0.5)
    pygame.quit()
    quit()

game_intro()
gameLoop()
