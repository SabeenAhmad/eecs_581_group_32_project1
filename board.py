'''
Author: Jenna Luong
Date: 9/10/25
Purpose:
External Sources:
'''

# Board definition

import random
from cell import Cell
from config import *
import pygame

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.gridSurface = pygame.Surface((WIDTH, HEIGHT))
        self.grid = [[Cell(r, c, 0) for c in range(cols)] for r in range(rows)]
        self.addMines()
        self.gameOver = False # bool to check if game over (mine clicked on grid)
        self.victory = False
        print(self.grid)

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                cell.draw(self.gridSurface)
        screen.blit(self.gridSurface, (0, 0))
            
    def addMines(self):
        for i in range(MINES):
            while True:
                row = random.randint(0, ROWS - 1)
                col = random.randint(0, COLS - 1)
                if self.grid[row][col].cellState == 0:
                    self.grid[row][col].cellState = 3
                    break
