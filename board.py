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
        self.gridSurface = pygame.Surface((WIDTH, HEIGHT - GAME_STATE_OBJ_SIZE))
        self.grid = [[Cell(r, c, 0) for c in range(cols)] for r in range(rows)]
        self.gameOver = False # bool to check if game over (mine clicked on grid)
        self.victory = False
        print(self.grid)

    def draw(self, screen):
    # Updated by Kit — 2025-09-15: clear once per frame (moved out of the loop)
        self.gridSurface.fill((210, 210, 210))

        for row in self.grid:
            for cell in row:
                cell.draw(self.gridSurface)

        screen.blit(self.gridSurface, (0, GAME_STATE_OBJ_SIZE))

            
    def addMines(self, safe_rc):
        # Updated by Kit — 2025-09-15: skip the first-clicked safe cell when placing mines
        safe_r, safe_c = safe_rc
        placed = 0
        while placed < MINES:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r == safe_r and c == safe_c):
                continue
            if self.grid[r][c].cellState == 0:
                self.grid[r][c].cellState = 3  # mine
            placed += 1

    def insertMines(self, safe_rc):
        # Updated by Kit — 2025-09-15: place mines away from safe cell and compute numbers once
        self.addMines(safe_rc)
        self.compute_adjacents()
        self.minesPlaced = True


    # Updated by Kit — 2025-09-15: count adjacent mines once after placement
    def compute_adjacents(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.cellState == 3:
                    cell.adjMines = 0
                    continue
                cnt = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc].cellState == 3:
                                cnt += 1
                cell.adjMines = cnt

