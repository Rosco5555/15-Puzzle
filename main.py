import numpy as np
from numpy.core.fromnumeric import squeeze
import pygame, sys, shelve
from pygame.locals import *
from timeit import default_timer as timer

### GLOBAL VARIABLES AND CONSTANTS
SCREENWIDTH = 800
SCREENHEIGHT = 800
WIDTH = 400
HEIGHT = 400
W = 200
H = 100
M = 7
X = (SCREENWIDTH / 2) - (W /2)
Y = (SCREENHEIGHT / 2) - (H / 2)
MARGIN = (SCREENWIDTH - WIDTH) / 2
SQUAREWIDTH = WIDTH / 4
WHITE = [255, 255, 255]
BLACK = [0,0,0]
RED   = [255, 0, 0]
THICKNESS = 2
GRID_DIM = 4
SOLVED_STATE = np.array([[1,2,3,4],
                        [5,6,7,8],
                        [9,10,11,12],
                        [13,14,15,0]])
CHECKER = np.array([[1,2,3,4],
                        [5,6,7,8],
                        [9,10,11,12],
                        [13,14,15,0]])




def findHole(array):
    for i in range(GRID_DIM - 1,-1,-1):
        for j in range(GRID_DIM - 1,-1,-1):
            if (array[i][j] == 0):
                return GRID_DIM - i

def countInversions(array):
    inversions = 0
    arr = []
    for y in array:
        for x in y:
            if (x != 0):
                arr.append(x)
    for i in range(0,len(arr)):
        for j in range(i+1, len(arr)):
                if (arr[j] and arr[i] and arr[i] > arr[j]):
                    inversions +=1
    return inversions

def isSolvable(puzzle):
    row = findHole(puzzle)
    inversions = countInversions(puzzle)
    if ((row % 2) == 1):
            if (inversions % 2 == 0):
                return True
            else:
                return False
    else:
        if (inversions % 2 == 1):
            return True
        else:
            return False


def makeState():
    while True:
        solved_state = SOLVED_STATE.ravel()
        np.random.shuffle(solved_state)
        solved_state = solved_state.reshape(4,4)
        if (isSolvable(solved_state)):
            return solved_state

def drawSquare(x ,y, n):
    pygame.draw.rect(screen, BLACK, pygame.Rect((MARGIN) + (x * SQUAREWIDTH), (MARGIN) + (y * SQUAREWIDTH), SQUAREWIDTH, SQUAREWIDTH))
    pygame.draw.rect(screen, RED, pygame.Rect((MARGIN) + (x * SQUAREWIDTH), (MARGIN) + (y * SQUAREWIDTH), SQUAREWIDTH - THICKNESS, SQUAREWIDTH - THICKNESS))
    text = font.render(str(n), True, BLACK)
    text_rect = text.get_rect(center=((MARGIN) + (x * SQUAREWIDTH) + (SQUAREWIDTH/2), (MARGIN) + (y * SQUAREWIDTH)+ (SQUAREWIDTH/2)))
    screen.blit(text, text_rect)



def drawGrid(array):
    for column in range(GRID_DIM):
        for row in range(GRID_DIM):
            value = array[row][column]
            if (value > 0):
                drawSquare(column, row, value)

def checkNeighbours(x,y,array):
    if (x + 1 < GRID_DIM):
        if (array[x+1][y] == 0):
            return (x+1,y)
    if (y + 1 < GRID_DIM):
        if (array[x][y+1] == 0):
            return (x,y+1)
    if (x - 1 >= 0):
        if (array[x-1][y] == 0):
            return (x-1, y)

    if (y - 1 >= 0):
        if (array[x][y-1] == 0):
            return (x, y-1)

    return (-1,-1)

def squareClicked(x,y, array):
    if (x < GRID_DIM and y < GRID_DIM):
        (i,j) = checkNeighbours(x,y,array)
        value = array[x][y]
        if (i != -1) and (j !=-1):
            array[x][y] = 0
            array[i][j] = value
        drawGrid(array)
        pygame.display.update()

def drawMenu(time, best):
    time = round(time, 3)
    best = round(best, 3)
    text_str = "Time: " + str(time)
    text_best = "Best Time: " + str(best)
    text_play_again = "Press SPACE to play again"
    text = menu_font.render(text_str, True, BLACK)
    bestTimeText = menu_font.render(text_best, True, BLACK)
    text_rect = text.get_rect(center=((SCREENWIDTH / 2)-50, (SCREENHEIGHT / 2) - 50))
    screen.blit(text, text_rect)
    best_text_rect = text.get_rect(center=((SCREENWIDTH / 2) -50, (SCREENHEIGHT / 2)))
    screen.blit(bestTimeText, best_text_rect)
    play_again_rect = text.get_rect(center=((SCREENWIDTH / 2) -50, (SCREENHEIGHT / 2) + 100))
    playAgainText = menu_font.render(text_play_again, True, BLACK)
    screen.blit(playAgainText, play_again_rect)



def drawStartMenu():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, pygame.Rect(X, Y, W, H))
    pygame.draw.rect(screen, RED, pygame.Rect(X + M, Y + M, W - (2 * M), H - (2 * M)))
    text = menu_font.render("4x4", True, BLACK)
    text_rect = text.get_rect(center=(X + (W /2), Y + (H / 2)))
    screen.blit(text, text_rect)


def handleTime(t):
    d = shelve.open('times.txt', writeback= True)
    best = d['time']
    if (t < best):
        d['time'] = t
        best = t
        d.close()
    return best

# GAME LOOP
pygame.init()
font = pygame.font.SysFont(None, 100)
menu_font = pygame.font.SysFont(None, 50)
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('15 Puzzle')
array = makeState()
solved = True
gameSelected = False
# Writing an initial time of 100000
d = shelve.open('times.txt')
if not 'time' in d:
    d['time'] = 10000

d.close()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not solved:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y =  pos[1]
                i = int((pos[0] - MARGIN) / SQUAREWIDTH)
                j = int((pos[1] - MARGIN) / SQUAREWIDTH)
                squareClicked(j,i,array)
                if (np.array_equal(CHECKER, array)):
                    end = timer()
                    time = end - start
                    screen.fill(WHITE)
                    best = handleTime(time)
                    drawMenu(time, best)
                    solved = True
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y =  pos[1]
            if ((X < x < (X + W)) and (Y < y < (Y + H)) and (not gameSelected)):
                    makeState()
                    start = timer()
                    solved = False
                    gameSelected = True

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                if solved:
                    makeState()
                    start = timer()
                    solved = False
        elif event.type == QUIT:
            running = False
    if (not solved):
        screen.fill(WHITE)
        drawGrid(array)
    elif (not gameSelected):
        drawStartMenu()

    pygame.display.update()

