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
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.isMine = False # bool to check if cell is mine
        self.isClicked = False # bool to check if cell is clicked
        self.isFlagged = False # bool to check if cell flagged
        self.adjMines = 0

    def draw(self, screen, font):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(screen, GRID_COLOR, rect)

        pygame.draw.rect(screen, (100, 100, 100), rect, 1)