import pygame
import random
from constants import *

def drawBoard(board, surface):
    for i in range(len(board)):
        for j in range(len(board[i])):
            cell = board[i][j]
            x = i * SIZE 
            y = j * SIZE
            if cell == 0:
                pygame.draw.rect(surface, BLACK, pygame.Rect(x, y, SIZE, SIZE))
            elif cell == 1:
                pygame.draw.rect(surface, WHITE, pygame.Rect(x, y, SIZE, SIZE))
            elif cell == 2:
                pygame.draw.rect(surface, GREEN, pygame.Rect(x, y, SIZE, SIZE))
            else:
                pygame.draw.rect(surface, RED, pygame.Rect(x, y, SIZE, SIZE))

def pickStart():
    borders = [0, 1, ROWS - 1, COLS - 1]
    idx = random.randint(0, 3)
    choice = borders[idx] 
    if choice == 0:
        x = 0
        y = random.randint(0, COLS - 1)
        endX = ROWS - 1
        endY = random.randint(1, COLS - 2)
    elif choice == 1:
        x = random.randint(0, ROWS - 1)
        y = 0
        endX = random.randint(1, ROWS - 2)
        endY = COLS - 1
    elif choice == ROWS - 1:
        x = ROWS - 1
        y = random.randint(0, COLS - 1)
        endX = 0
        endY = random.randint(1, COLS - 2)
    else:
        x = random.randint(0, ROWS - 1)
        y = COLS - 2
        endX = random.randint(1, ROWS - 2)
        endY = 0  
    return ((x, y), (endX, endY))

def isValid(x, y):
    return x >= 0 and x < COLS and y >= 0 and y < ROWS

def getNeighbors(x, y):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            dx = x + i
            dy = y + j
            one = abs(i) == 1
            two = abs(j) == 1
            
            if (isValid(dx, dy) and (dx != x or dy != y) and (one ^ two)):
                neighbors.append((dx, dy))
    
    return neighbors

def getFrontiers(x, y):
    frontiers = []
    for i in range(4):
        dx = x
        dy = y
        if i == 0:
            dx += 2
        elif i == 1:
            dx -= 2
        elif i == 2:
            dy += 2
        else:
            dy -= 2
        if (isValid(dx, dy)):
            frontiers.append((dx, dy))


    return frontiers

def clearAroundExit(maze: list[list[int]], x:int, y:int):
    if x == 0:
        maze[y][x+1] = 1
    elif x == ROWS - 1:
        maze[y][x-1] = 1
    elif y == 0:
        maze[y+1][x] = 1
    elif y == COLS - 1:
        maze[y-1][x] = 1

def createPath(maze: list[list[int]], startX:int, startY:int, endX:int, endY:int):
    choice = random.randint(1,4)
    x = startX
    y = startY
    while x != endX and y != endY:
        if choice == 1:
            x += 1
        elif choice == 2:
            x -= 1
        elif choice == 3:
            y += 1
        else:
            y -= 1
        if isValid(x, y):
            cell = maze[y][x]
            if cell != 0 and cell != 3:
                cell = 1
def mazeGeneration(maze: list):
    res = pickStart()
    x, y = res[0]
    endX, endY = res[1] 
    maze[y][x] = 2
    maze[endY][endX] = 3
    clearAroundExit(maze, endX, endY)
    createPath(maze, x, y, endX, endY) 
    frontiers = getFrontiers(x, y) 
    
    while(len(frontiers) > 0):
        idx = random.randint(0, len(frontiers) - 1)
        frontierX, frontierY= frontiers[idx]
        neighbors = []
        for nx, ny in getFrontiers(frontierX, frontierY):
            if maze[ny][nx] != 0:
                neighbors.append((nx, ny))

        if neighbors:
            idx = random.randint(0, len(neighbors) - 1)
            nx, ny = neighbors[idx]
            maze[(frontierY + ny) // 2][(frontierX + nx) // 2] = 1
            maze[frontierY][frontierX] = 1

            for fx, fy in getFrontiers(frontierX, frontierY):
                if maze[fy][fx] == 0 and (fx, fy) not in frontiers:
                    frontiers.append((fx, fy))
        
        frontiers.remove((frontierX, frontierY))

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generation")
running = True

#0 denotes a wall
#1 denotes a path
maze = [[0 for i in range(COLS)] for j in range(ROWS)]
mazeGeneration(maze)

while running:
    surface.fill(BLACK)
    x, y = pygame.mouse.get_pos()
    row = x // SIZE
    col = y // SIZE
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            print(pickStart())

    drawBoard(maze, surface)
    pygame.display.update() 

pygame.quit()