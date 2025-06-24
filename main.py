import pygame
import random
import copy
import time 
from collections import deque 
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
            elif cell == 3:
                pygame.draw.rect(surface, RED, pygame.Rect(x, y, SIZE, SIZE))
            elif cell == 4:
                pygame.draw.rect(surface, YELLOW, pygame.Rect(x, y, SIZE, SIZE))

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
        if isValid(x+1,y+1):
            maze[y+1][x+1] = 1
        if isValid(x+1,y-1):
            maze[y-1][x+1] = 1
    elif x == ROWS - 1:
        maze[y][x-1] = 1
        if isValid(x-1,y+1):
            maze[y+1][x-1] = 1
        if isValid(x-1,y-1):
            maze[y-1][x-1] = 1
    elif y == 0:
        maze[y+1][x] = 1
        if isValid(x+1,y+1):
            maze[y+1][x+1] = 1
        if isValid(x-1,y-1):
            maze[y+1][x-1] = 1
    elif y == COLS - 1:
        maze[y-1][x] = 1
        if isValid(x+1,y-1):
            maze[y-1][x+1] = 1
        if isValid(x-1,y-1):
            maze[y-1][x-1] = 1

def findEnd(maze: list[list[int]], startX:int, startY:int):
    candidates = []
    for x in range(COLS):
        if maze[0][x] == 1:
            candidates.append((x, 0))
        elif maze[ROWS - 1][x] == 1:
            candidates.append((x, ROWS - 1))

    for y in range(ROWS):
        if maze[y][0] == 1:
            candidates.append((0, y))
        elif maze[y][COLS - 1] == 1:
            candidates.append((COLS - 1, y))

    for i in candidates:
        if i[1] == startY or i[0] == startX:
            candidates.remove(i)

    return random.choice(candidates)

def dfs(maze:list[list[int]], startX:int, startY:int) -> list[tuple[int,int]]:
    newMaze = copy.deepcopy(maze) 
    positions = []
    stack = deque()
    newMaze[startY][startX] = 4 
    stack.append((startX, startY))
    
    while len(stack) > 0:
        x, y = stack.pop()
        if newMaze[y][x] == 3:
            return positions
        if (x,y) != (startX, startY):
            positions.append((x,y))
        
        neighbors = getNeighbors(x, y)
        for i in neighbors:
            if newMaze[i[1]][i[0]] == 1:
                newMaze[i[1]][i[0]] = 4
                stack.append((i[0],i[1]))
            elif newMaze[i[1]][i[0]] == 3:
                stack.append((i[0], i[1]))
    return positions

def mazeGeneration(maze: list):
    res = pickStart()
    x, y = res[0]
    endX, endY = res[1] 
    maze[y][x] = 2
    clearAroundExit(maze, endX, endY)
    frontiers = set(getFrontiers(x, y))
    
    while(len(frontiers) > 0):
        frontierX, frontierY= random.choice(list(frontiers))
        neighbors = []
        for nx, ny in getFrontiers(frontierX, frontierY):
            if maze[ny][nx] == 1 or maze[ny][nx] == 2:
                neighbors.append((nx, ny))

        if neighbors:
            idx = random.randint(0, len(neighbors) - 1)
            nx, ny = neighbors[idx]
            maze[(frontierY + ny) // 2][(frontierX + nx) // 2] = 1
            maze[frontierY][frontierX] = 1

            for fx, fy in getFrontiers(frontierX, frontierY):
                if maze[fy][fx] == 0:
                    frontiers.add((fx, fy))
        
        frontiers.discard((frontierX, frontierY))
    
    endX, endY = findEnd(maze, x, y)
    maze[endY][endX] = 3
    return res[0]

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generation")
running = True

#0 denotes a wall
#1 denotes a path
#2 denotes the start
#3 denotes the end
#4 denotes visited
maze = [[0 for i in range(COLS)] for j in range(ROWS)]
startX, startY = mazeGeneration(maze)
counter = 0
dfsPositions = []

while running:
    surface.fill(BLACK)
    x, y = pygame.mouse.get_pos()
    row = x // SIZE
    col = y // SIZE
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            dfsPositions = dfs(maze, startX, startY)
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_b:
                for x, y in dfsPositions:
                    counter += 1
                    maze[y][x] = 4 
                    drawBoard(maze, surface)
                    pygame.display.update()
                    time.sleep(0.001)

    drawBoard(maze, surface)
    pygame.display.update() 

pygame.quit()