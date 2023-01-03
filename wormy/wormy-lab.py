# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
import time

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
YELLOW = (255, 255, 0)  # REQUIREMENT No. 2
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


counter = 0  # REQUIREMENT 1
direction2 = LEFT  # REQUIREMENT 1
points = 0  # REQUIREMENT 2

def runGame():
    global counter, direction2, points  # REQUIREMENT 1,2

    startTime = time.time()  # REQUIREMENT 1 ADDED TIMER
    counterObj1 = 10
    counterObj2 = 10
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    startx2 = random.randint(5, CELLWIDTH - 6)  # REQUIREMENT 1 ADDED THE INITIAL COORDINATES FOR THE NEW WORM
    starty2 = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    wormCoords2 = [{'x': startx2,     'y': starty2},  # REQUIREMENT 1 ADDED COORDINATES FOR THE SECOND WORM
                   {'x': startx2 - 1, 'y': starty2},
                   {'x': startx2 - 2, 'y': starty2}]
    direction = RIGHT
    # Start the apple in a random place.
    apple = getRandomLocation()
    object1 = {'x': -1, 'y': -1} # REQUIREMENT 2 setting initial position to an invisible place
    object2 = {'x': -1, 'y': -1} # REQUIREMENT 2 setting initial position to an invisible place
    object1Location = {'x': -1, 'y': -1} # REQUIREMENT 2 setting initial position to an invisible place
    object2Location = {'x': -1, 'y': -1} # REQUIREMENT 2 setting initial position to an invisible place

    while True: # main game loop
        counterObj1 -= 1 # REQUIREMENT 2 setting a counter so the first object appears at random intervals
        counterObj2 -= 1 # REQUIREMENT 2 setting a counter so the second object appears at random intervals
        if counterObj1 == 0:
            object1 = getRandomLocation() # REQUIREMENT 2
            object1Location = object1
            counterObj1 = - 10

        if counterObj2 == 0:
            object2 = getRandomLocation() # REQUIREMENT 2
            object2Location = object2

        if int(pygame.time.get_ticks() / 1000) % 2 == 0 and int(pygame.time.get_ticks() / 1000) < 7:  # REQUIREMENT 2
            object1 = {'x': -1, 'y': -1}
            object2 = {'x': -1, 'y': -1}
        elif object1['x'] != -2 and object1['y'] != -2 and object2['x'] != -2 and object2['y'] != -2:
            object1 = object1Location
            object2 = object2Location

        if int(pygame.time.get_ticks() / 1000) > 7:  # REQUIREMENT 2
            object1 = {'x': -1, 'y': -1}  # making the object disappear after 7 seconds/it appears only once

        if int(pygame.time.get_ticks() / 1000) % 5 == 0:  # REQUIREMENT 2
            if int(pygame.time.get_ticks() / 1000) % 2 == 0:
                object2 = {'x': -1, 'y': -1}
            elif object2['x'] != -2 and object2['y'] != -2:
                drawObject(getRandomLocation())
                object2 = object2Location

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
                elif event.key == K_ESCAPE:
                    terminate()

        if counter % 10 == 0:
            direction2 = random.choice((LEFT, RIGHT, UP, DOWN))  # REQUIREMENT 1 ADDING RANDOM DIRECTION TO THE NEW WORM
        counter += 1

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        if wormCoords2[HEAD]['x'] == -1 or wormCoords2[HEAD]['x'] == CELLWIDTH or wormCoords2[HEAD]['y'] == -1 or wormCoords2[HEAD]['y'] == CELLHEIGHT:
            # REQUIREMENT 1 CHANGING THE DIRECTIONS OF THE NEW WORM RANDOMLY IF IT HITS THE CORNERS
            dirs = [LEFT, RIGHT, UP, DOWN]
            dirs.remove(direction2)
            direction2 = random.choice(dirs)

        # check if worm has eaten an apply
        # if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        elif object1['x'] != -1 and object1['y'] != -1 and wormCoords[HEAD]['x'] == object1['x'] and wormCoords[HEAD]['y'] == object1['y']:
            points += 3
            object1 = {'x': -2, 'y': -2}  # making the object disappear
        elif object2['x'] != -1 and object2['y'] != -1 and wormCoords[HEAD]['x'] == object2['x'] and wormCoords[HEAD]['y'] == object2['y']:
            points += 3
            object2 = {'x': -2, 'y': -2}  # making the object disappear
        else:
            # REQUIREMENT 1 ADDING A CONDITION TO SEE IF THE ORIGINAL WORM TOUCHES THE OTHER WITH ITS HEAD
            if not (wormCoords[HEAD]['x'] == wormCoords2[HEAD+1]['x'] and wormCoords[HEAD]['y'] == wormCoords2[HEAD+1]['y']):
                del wormCoords[-1]  # remove worm's tail segment

        # check if worm has eaten an apply
        if wormCoords2[HEAD]['x'] == apple['x'] and wormCoords2[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            # REQUIREMENT 1 ADDING A CONDITION TO SEE IF THE NEW WORM TOUCHES THE ORIGINAL WORM WITH ITS HEAD
            if not (wormCoords[HEAD + 1]['x'] == wormCoords2[HEAD]['x'] and wormCoords[HEAD + 1]['y'] == wormCoords2[HEAD]['y']):
                del wormCoords2[-1] # remove worm's tail segment

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

        # REQUIREMENT 1 move the NEW worm by adding a segment in the direction it is moving
        if direction2 == UP:
            newHead2 = {'x': wormCoords2[HEAD]['x'], 'y': wormCoords2[HEAD]['y'] - 1}
        elif direction2 == DOWN:
            newHead2 = {'x': wormCoords2[HEAD]['x'], 'y': wormCoords2[HEAD]['y'] + 1}
        elif direction2 == LEFT:
            newHead2 = {'x': wormCoords2[HEAD]['x'] - 1, 'y': wormCoords2[HEAD]['y']}
        elif direction2 == RIGHT:
            newHead2 = {'x': wormCoords2[HEAD]['x'] + 1, 'y': wormCoords2[HEAD]['y']}

        wormCoords2.insert(0, newHead2)

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        if time.time() - startTime > 20:  # REQUIREMENT 1 DRAWING THE NEW WORM 20 SECONDS AFTER THE GAME HAS STARTED
            drawWorm(wormCoords2)
        drawApple(apple)
        if object1['x'] != -1 and object1['y'] != -1 and object1['x'] != -2 and object1['y'] != -2: # REQUIREMENT 2
            drawObject(object1)
        if object2['x'] != -1 and object2['y'] != -1 and object2['x'] != -2 and object2['y'] != -2: # REQUIREMENT 2
            drawObject(object2)
        drawScore(len(wormCoords) - 3 + points)
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
    global points

    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)  # REQUIREMENT 2 MODIFIED
    buttonFont = pygame.font.Font('freesansbold.ttf', 20)  # REQUIREMENT 3

    resetSurf = buttonFont.render('Start from the beginning', True, WHITE)  # REQUIREMENT 3
    quitSurf = buttonFont.render('Quit', True, WHITE)  # REQUIREMENT 3
    resetRect = resetSurf.get_rect()  # REQUIREMENT 3
    quitRect = quitSurf.get_rect()  # REQUIREMENT 3
    resetRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT - 100)  # REQUIREMENT 3
    quitRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)  # REQUIREMENT 3

    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    pointsSurf = gameOverFont.render('+' + str(points) + ' extra pts', True, WHITE)  # REQUIREMENT 2
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    pointsRect = pointsSurf.get_rect()  # REQUIREMENT 2
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    pointsRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 150)  # REQUIREMENT 2
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    DISPLAYSURF.blit(pointsSurf, pointsRect)  # REQUIREMENT 2
    DISPLAYSURF.blit(resetSurf, resetRect)  # REQUIREMENT 3
    DISPLAYSURF.blit(quitSurf, quitRect)  # REQUIREMENT 3
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue
    # Store the option buttons and their rectangles in OPTIONS.

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP:  # REQUIREMENT 3
                if quitRect.collidepoint(event.pos):
                    terminate()
                elif resetRect.collidepoint(event.pos):
                    runGame()
                    showGameOverScreen()

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawObject(coord):  # REQUIREMENT 2 the function for drawing a new element
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, YELLOW, appleRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()