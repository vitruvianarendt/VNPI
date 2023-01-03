# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
YELLOW    = (255, 255,   0)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head
HEAD2 = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, NEW_SURF, NEW_RECT, QUIT_SURF, QUIT_RECT                           #Requirement 3

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    NEW_SURF, NEW_RECT = text('Start from the beginning', WHITE, GREEN, WINDOWWIDTH - 250,WINDOWHEIGHT - 90)    #Requirement 3
    QUIT_SURF, QUIT_RECT = text('Quit', WHITE, GREEN, WINDOWWIDTH - 75, WINDOWHEIGHT - 60)                      #Requirement 3

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    score = len(wormCoords) - 3                                         #Requirement 2
    

    # Set a random start point for the second worm.
    startx2 = random.randint(5, CELLWIDTH - 6)                          #Requirement 1
    starty2 = random.randint(5, CELLHEIGHT - 6)                         #Requirement 1
    second_worm_coords = [{'x': startx2, 'y': starty2},                 #Requirement 1
                          {'x': startx2 - 1, 'y': starty2},             #Requirement 1
                          {'x': startx2 - 2, 'y': starty2}]             #Requirement 1

    # Start the apple in a random place.
    apple = getRandomLocation()
    apple2Coords = getRandomLocation()                                 #Requirement 2
    apple3Coords = getRandomLocation()                                 #Requirement 2

    # adding a timer for the second worm
    start_time = pygame.time.Clock()
    elapsed_time = 0


    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif NEW_RECT.collidepoint(event.pos):                  #Requirement 3
                    showStartScreen()                                   #Requirement 3
                elif QUIT_RECT.collidepoint(event.pos):                 #Requirement 3
                    terminate()                                         #Requirement 3
                elif event.key == K_ESCAPE:
                    terminate()

        # if elapsed_time % 9==0:
        #     #nacrtaj go vtoriot crv
        #     directions = [UP, DOWN, LEFT, RIGHT]
        #     direction2 = UP;
        #     if random.randint(0,100) % 17:
        #         direction2 = random.choice(directions)
        #     if direction2 == UP:
        #         newHead2 = {'x': second_worm_coords[HEAD2]['x'], 'y': second_worm_coords[HEAD2]['y'] - 1}
        #     elif direction2 == DOWN:
        #         newHead2 = {'x': second_worm_coords[HEAD2]['x'], 'y': second_worm_coords[HEAD2]['y'] + 1}
        #     elif direction2 == LEFT:
        #         newHead2 = {'x': second_worm_coords[HEAD2]['x'] - 1, 'y': second_worm_coords[HEAD2]['y']}
        #     elif direction2 == RIGHT:
        #         newHead2 = {'x': second_worm_coords[HEAD2]['x'] + 1, 'y': second_worm_coords[HEAD2]['y']}
        #     second_worm_coords.pop()
        #     second_worm_coords.insert(0, newHead2)

        #Create a moveset for the second worm.
        secondWorm = [{'x': second_worm_coords[HEAD2]['x'], 'y': second_worm_coords[HEAD2]['y'] - 1},       #Requirement 1
                        {'x': second_worm_coords[HEAD2]['x'], 'y': second_worm_coords[HEAD2]['y'] + 1},     #Requirement 1
                        {'x': second_worm_coords[HEAD2]['x'] - 1, 'y': second_worm_coords[HEAD2]['y']},     #Requirement 1
                        {'x': second_worm_coords[HEAD2]['x'] + 1, 'y': second_worm_coords[HEAD2]['y']}]     #Requirement 1

        if random.randint(0,100) % 17 == 0:                                                                 #Requirement 1
            secondWormHead = random.choice(secondWorm)                                                      #Requirement 1
            second_worm_coords.insert(0, secondWormHead)                                                    #Requirement 1
            del second_worm_coords[-1]                                                                      #Requirement 1

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        #this is so that the second worm object does not collide with our worm untill 20 seconds have passed and the second womr starts being active
        if int(pygame.time.get_ticks() / 1000) >= 20:                                                                                       #Requirement 1
            # if we hit the second worm gameover?
            if wormCoords[HEAD]['x'] == second_worm_coords[HEAD2]['x'] and wormCoords[HEAD]['y'] == second_worm_coords[HEAD2]['y']:         #Requirement 1
                return # game over                                                                                                          #Requirement 1
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over
        #this is so that the second worm object does not collide with our worm untill 20 seconds have passed and the second womr starts being active
        if int(pygame.time.get_ticks() / 1000) >= 20:                                                                                       #Requirement 1
            # if we hit the second worm gameover?
            for wormBody2 in second_worm_coords[1:]:                                                                                        #Requirement 1
                if wormBody2['x'] == wormCoords[HEAD]['x'] and wormBody2['y'] == wormCoords[HEAD]['y']:                                     #Requirement 1
                    return

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y'] :
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
            if random.randint(0,100) % 17 == 0:
                apple2Coords = getRandomLocation()
            if random.randint(0,100) % 16 == 0:
                apple3Coords = getRandomLocation()
        else:
            del wormCoords[-1] # remove worm's tail segment

        #Check if the player wom has eaten one of the new apples
        if wormCoords[HEAD]['x'] == apple2Coords['x'] and wormCoords[HEAD]['y'] == apple2Coords['y'] :               #Requirement 2
            # don't remove worm's tail segment
            apple2Coords = getRandomLocation() # set a new apple somewhere                                           #Requirement 2
            score += 3                                                                                               #Requirement 2

        # Check if the player wom has eaten one of the new apples
        if wormCoords[HEAD]['x'] == apple3Coords['x'] and wormCoords[HEAD]['y'] == apple3Coords['y']:                #Requirement 2
            # don't remove worm's tail segment
            apple3Coords = getRandomLocation()  # set a new apple somewhere                                          #Requirement 2
            score += 3                                                                                               #Requirement 2

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords, GREEN)
        #Flag for drawing the second worm object
        flag = 0
        if int(pygame.time.get_ticks() / 1000) >= 20:                   #Requirement 1
            flag = 1                                                    #Requirement 1
            if flag:                                                    #Requirement 1
                drawWorm(second_worm_coords, RED)                       #Requirement 1
        drawApple(apple)
        drawScore(len(wormCoords) - 3 + score)                          #Requirement 2
        time = int(pygame.time.get_ticks() / 1000)                      #Requirement 2
        if time % 5 <= 2 and time % 10 != 2:                            #Requirement 2
            drawNewApples(apple3Coords, WHITE)                          #Requirement 2
        else:                                                           #Requirement 2
            apple3Coords = {'x': -101, 'y': -101}                       #Requirement 2
        if 0 < time < 7:                                                #Requirement 2
            drawNewApples(apple2Coords, YELLOW)                         #Requirement 2
        else:                                                           #Requirement 2
            apple2Coords = {'x': -100, 'y': -100}                       #Requirement 2
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    global NEW_SURF, NEW_RECT, QUIT_SURF, QUIT_RECT                     #Requirement 3
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)                                          #Requirement 3
    DISPLAYSURF.blit(QUIT_SURF, QUIT_RECT)                                        #Requirement 3
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

#Modify the function to have a variable color for each worm
def drawWorm(wormCoords, color):                #Requirement 1
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, color, wormInnerSegmentRect)          #Requirement 1 #Use the color defined in the function call rather than the predefined one


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))



def drawNewApples(coord, color=None):                                   #Requirement 2
    x = coord['x'] * CELLSIZE                                           #Requirement 2
    y = coord['y'] * CELLSIZE                                           #Requirement 2
    elementRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)                 #Requirement 2
    pygame.draw.rect(DISPLAYSURF, color, elementRect)                   #Requirement 2


def text(text, color, bgcolor, top, left):                              #Requirement 3
    textSurf = BASICFONT.render(text, True, color, bgcolor)             #Requirement 3
    textRect = textSurf.get_rect()                                      #Requirement 3
    textRect.topleft = (top, left)                                      #Requirement 3
    return (textSurf, textRect)                                         #Requirement 3

if __name__ == '__main__':
    main()