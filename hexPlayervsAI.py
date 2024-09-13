import pygame,sys
import numpy as np
from pygame import draw
from pygame.draw import circle
from turtle import *
from math import inf
from heapq import heappush, heappop
from string import ascii_uppercase
from collections import OrderedDict
import time
import tkinter as tk
from tkinter import messagebox



BORDER_LINE_WIDTH = 2
INSIDE_LINE_WIDTH = 1
DEPTH = 2  
RED = (255,0,0) 
BLUE = (0,0, 255)  
BG_COLOR = (28,170,156)  
LINE_COLOR = (23, 145, 135)  

def draw_figures(screen, a, BOARD_SIZE):
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if a[row][col] == '2':
                
                pygame.draw.rect(screen, RED, [int(col*50 + 50), int(row*50 + 50), 50, 50])
            elif a[row][col] == '1':
                
                pygame.draw.rect(screen, BLUE, [int(col*50 + 50), int(row*50 + 50), 50, 50])

def available_square(a, row, col):
   
    if a[row][col] == '0':
        return True
    else:
        return False

def draw_lines(screen, BOARD_SIZE):
    
    START = 100  
    for i in range(BOARD_SIZE - 1):
       
        pygame.draw.line(screen, LINE_COLOR, (50, START + 50*i), (50*(BOARD_SIZE + 1), START + 50*i), INSIDE_LINE_WIDTH)
       
        pygame.draw.line(screen, LINE_COLOR, (START + 50*i, 50), (START + 50*i, 50*(BOARD_SIZE + 1)), INSIDE_LINE_WIDTH)
    
   
    pygame.draw.line(screen, BLUE, (50, 50), (50, 50*(BOARD_SIZE + 1)), BORDER_LINE_WIDTH)
    pygame.draw.line(screen, BLUE, (50*(BOARD_SIZE + 1), 50), (50*(BOARD_SIZE + 1), 50*(BOARD_SIZE + 1)), BORDER_LINE_WIDTH)
    pygame.draw.line(screen, RED, (50, 50), (50*(BOARD_SIZE + 1), 50), BORDER_LINE_WIDTH)
    pygame.draw.line(screen, RED, (50, 50*(BOARD_SIZE + 1)), (50*(BOARD_SIZE + 1), 50*(BOARD_SIZE + 1)), BORDER_LINE_WIDTH)

def check_win(a, player):
    
    if gameStatus(a, '1'):
        return True  
    elif gameStatus(a, '2'):
        return True  
    return False

def restart(screen, a, BOARD_SIZE):
    
    screen.fill(BG_COLOR)  
    draw_lines(screen, BOARD_SIZE)  
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            a[row][col] = '0'
            
def positions(i, j, n):
    """
    Generates a list of adjacent positions for a given cell in a grid.
    Diagonal connections are considered based on grid boundaries.

    Args:
    i (int): The row index of the current cell.
    j (int): The column index of the current cell.
    n (int): The dimension of the square grid (n x n).

    Returns:
    list: A list of tuples, each representing an adjacent cell position.
    """
    positionArr = []
    
    if i is not 0:
        positionArr.append([i - 1, j])  
        if j is not n - 1:
            positionArr.append([i - 1, j + 1])  

    
    if i is not n - 1:
        positionArr.append([i + 1, j])  
        if j is not 0:
            positionArr.append([i + 1, j - 1])  

    
    if j is not 0:
        positionArr.append([i, j - 1])  
    if j is not n - 1:
        positionArr.append([i, j + 1])  

    return positionArr


def vacantPlaces(a):
    """
    Finds all unoccupied (vacant) places on the game board.

    Args:
    a (list): 2D list representing the game board.

    Returns:
    list: A list of tuples representing vacant positions in the format (row, column).
    """
    nextList = []
    for i in range(len(a)):
        for j in range(len(a)):
            if a[i][j] is '0': 
                pairs = (chr(65 + i), j)  
                nextList.append(pairs)
    return nextList


def check(a, x, player, visited):
    """
    Recursively checks for a winning path starting from a specific cell.

    Args:
    a (list): 2D list representing the game board.
    x (tuple): Current cell coordinates (row, column).
    player (str): Current player's marker.
    visited (dict): Dictionary of visited cells to avoid revisits.

    Returns:
    int: 302 if a winning path is found, otherwise 404.
    """
    
    if a[x[0]][x[1]] == str(player):
        
        pathList = positions(x[0], x[1], len(a))

        
        for y in pathList:
            
            if str(y) not in visited.keys():
               
                if a[y[0]][y[1]] == str(player):
                    
                    visited[str(y)] = True

                    
                    
                    if y[1] == len(a) - 1:
                        return 302  

                    
                    val = check(a, y, player, visited)
                    
                    if val == 302:
                        return 302

    
    return 404



def gameStatus(a, player):
    """
    Determines if the specified player has won by checking all possible paths.

    Args:
    a (list): 2D list representing the game board.
    player (str): The marker of the current player.

    Returns:
    bool: True if the player has won, otherwise False.
    """
    transpose = [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]
    if player == '2':
        a = transpose  # Transpose the board to check vertical paths horizontally
    firstList = [(j, 0) for j in range(len(a))]  # Start points for checking paths
    for i in firstList:
        visited = {str([i[0], i[1]]): True}
        result = check(a, i, player, visited)
        if result == 302:
            return True
    return False

def score(val, player):
    """
    Determines the scoring for a cell based on its current occupant relative to the player.

    Args:
    val (str): The current occupant of the cell ('0' for empty, '1' or '2' for players).
    player (str): The marker of the player evaluating the board.
    

    Returns:
    int: 1 for empty cells, making them more attractive strategically; 0 for cells occupied by the player, 
         indicating no benefit from re-visiting.
    """
    if val == '0':
        return 1  # Unoccupied cells score higher to encourage exploration.
    elif val == player:
        return 0  # Cells occupied by the player offer no additional score.
def h(a, player):
   
   
    transpose = [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]
    if player == '2':
        a = transpose
    
   
    parents = [(j, 0) for j in range(len(a))]
    
    
    visited = {}
    
   
    priorityQ = []
    
    
    n = len(a)
    
   
    for pair in parents:
        val = score(a[pair[0]][pair[1]], player)
        if a[pair[0]][pair[1]] == '0':
            visited[str(pair[0]) + str(pair[1])] = 1
            heappush(priorityQ, (1, str(pair[0]) + str(pair[1])))
        elif a[pair[0]][pair[1]] == player:
            visited[str(pair[0]) + str(pair[1])] = 0
            heappush(priorityQ, (0, str(pair[0]) + str(pair[1])))
    
   
    while priorityQ:
        parent = heappop(priorityQ)
        parentPos = parent[1]
        parentVal = parent[0]
        
       
        if parentPos[1] == str(n - 1):
            return parentVal
        
       
        children = positions(int(parentPos[0]), int(parentPos[1]), n)
        for child in children:
            temp = score(a[child[0]][child[1]], player)
            if temp is not None:
                val = parentVal + temp
                
                if str(child[0]) + str(child[1]) not in visited.keys() or visited[str(child[0]) + str(child[1])] > val:
                    val = parentVal + score(a[child[0]][child[1]], player)
                    visited[str(child[0]) + str(child[1])] = val
                    heappush(priorityQ, (val, str(child[0]) + str(child[1])))

 
def minimax(a, d, player1, player2, start):
    """
    Implements the Minimax algorithm to determine the best move for the current player based on a recursive analysis of potential future game states.
    
    Args:
    a (list): Current state of the game board, a 2D list.
    d (int): Remaining depth of recursion the algorithm will explore.
    player1 (str): Marker for Player 1.
    player2 (str): Marker for Player 2.
    start (str): Marker for the player whose turn it is to move.

    Returns:
    tuple: A tuple containing the maximum score achievable and the best move's position as ('score', 'position').
    """
    
    h1 = h(a, player2)
    
    if h1 == 0:
        
        if player2 == start:
            return 1000, '99'  
        else:
            return -1000, '99'  
    
    
    if d <= 0:
        h2 = h(a, player1)
        return h1 - h2, '99' 

    
    else:
        
        seats = vacantPlaces(a)
        valList = OrderedDict()  
        
        
        for pair in seats:
            x = ord(pair[0]) - 65  
            y = int(pair[1])        
            newA = list(map(list, a))  
            newA[x][y] = player1       
            
            
            # print(d)
            val, kkl = minimax(newA, d - 1, player2, player1, start)
            valList[str(x) + str(y)] = val 
        
        
        if player1 is start:
            
            pos = sorted(valList.items(), key=lambda bla: bla[1], reverse=True)[0]
            maxVal = pos[1]
            return maxVal, pos[0]  
        else:
            
            pos = sorted(valList.items(), key=lambda bla: bla[1])[0]
            minVal = pos[1]
            return minVal, pos[0]  
def start(a, n, d):
    
    BOARD_SIZE = n  
    WIDTH = (n + 2) * 50  
    HEIGHT = (n + 2) * 50  
    pygame.init()  
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  
    pygame.display.set_caption('HEX Player vs AI') 
    screen.fill(BG_COLOR)  
    
    draw_lines(screen, BOARD_SIZE)  

    
    player1 = '1'  
    player2 = '2' 
    steps = OrderedDict()  
    player = 1  
    game_over = False  

    
    while True:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                sys.exit()

           
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]  
                mouseY = event.pos[1]  
                x = int((mouseY - 50) // 50)  
                y = int((mouseX - 50) // 50)  

                
                if available_square(a, x, y):
                    a[x][y] = str(player1)  
                    player1, player2 = player2, player1  
                    if(gameStatus(a, '1')): 
                        game_over = True
                        
                        
                        
                        print("Player 1 Won!")
                    player = 2  
                    draw_figures(screen, a, BOARD_SIZE)  

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart(screen, a, BOARD_SIZE)  
                    start(a, n, d) 

                if event.key == pygame.K_i:
                    val, pos = minimax(a, d, player1, player2, player1) 
                    x = int(pos[0])
                    y = int(pos[1])
                    a[x][y] = str(player1)  
                    player1, player2 = player2, player1  
                    if(gameStatus(a, '2')):  
                        game_over = True
                        print("Player 2 Won!")
                    player = 1  
                    draw_figures(screen, a, BOARD_SIZE)  
                    

        pygame.display.update()  
def main():
    
    root=tk.Tk()
    root.withdraw()
    try:
        n = int(input("Enter the board size n: ")) 
        d = int(input("Enter the level of the game d: "))  

        
        a = [['0' for _ in range(n)] for _ in range(n)]
        print("A new game board of size {}x{} has been created:".format(n, n))
        for row in a:
            print(" ".join(row))  

        start(a, n, d)  

    except ValueError as e:  
        print("Invalid input! Please enter valid integers for board size and game level.")
    except Exception as e:  
        print("An unexpected error occurred:", str(e))

if __name__ == "__main__":
    main()  
