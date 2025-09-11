# Cell Definition

import pygame
from config import *

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.isMine = False
        self.isRevealed = False
        self.isFlagged = False
        self.adjMines = 0

    def draw(self, screen, font):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(screen, GRID_COLOR, rect)

        pygame.draw.rect(screen, (100, 100, 100), rect, 1)