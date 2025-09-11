'''
Author: 
Date:
Purpose:
External Sources:
'''

# Cell Definition

import pygame
from config import *

class Cell:
    def __init__(self, row, col, cellState):
        self.row = row
        self.rowSize = row * CELL_SIZE
        self.col = col
        self.colSize = col * CELL_SIZE
        self.cellState = cellState
        self.isClicked = False # bool to check if cell is clicked
        self.isFlagged = False # bool to check if cell flagged
        self.adjMines = 0

    def draw(self, gridSurface):
        rect = pygame.Rect(self.rowSize, self.colSize, CELL_SIZE, CELL_SIZE)

        if self.cellState == 0:
            color = (GRID_COLOR)
        elif self.cellState == 3:
            color = (BOMB_COLOR)
        else:
            color = (0, 0, 0)

        pygame.draw.rect(gridSurface, color, rect)
        pygame.draw.rect(gridSurface, (0, 0, 0), rect, 1)