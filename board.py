'''
File: board.py
Authors: Jace Keagy, K Li, Ian Lim, Jenna Luong, Kit Magar, Bryce Martin.
Date: 9/10/25
Purpose: Create & manage 2D grid, insert mines, compute adjacent mines, 
calculates mines left, check if victory.
External Sources: None.
'''

# Imports.
import random
from cell import Cell
from config import *
import pygame

# Class for handing the board.
class Board:
    def __init__(self, rows, cols):
        self.rows = rows # number of rows
        self.cols = cols # number of cols
        self.gridSurface = pygame.Surface((WIDTH, HEIGHT - GAME_STATE_OBJ_SIZE)) # grid surface with PyGame
        self.grid = [[Cell(r, c, 0) for c in range(cols)] for r in range(rows)] # Fills grid with proper row and col count with '0' cell state.
        self.gameOver = False # bool to check if game over (mine clicked on grid)
        self.victory = False # bool to check if won
    
    # Calculate flag count by subtracting flags from mines
    def flag_count(self):
        flags = sum(cell.isFlagged for row in self.grid for cell in row)
        return max(MINES - flags, 0)

    # Draws the board.
    def draw(self, screen):
        # Clear once per frame (moved out of the loop)
        self.gridSurface.fill((210, 210, 210))
        for row in self.grid:
            for cell in row:
                cell.draw(self.gridSurface)
        screen.blit(self.gridSurface, (0, GAME_STATE_OBJ_SIZE))
        # Renders how many flags are placed.
        font = pygame.font.SysFont(None, 36)
        flags_text = font.render(f"Flag count: {self.flag_count()}", True, (0, 0, 0))
        screen.blit(flags_text, (10, 10))

        # Render how many mines there are total
        mines_text = font.render(f"Mine count: {MINES}", True, (0, 0, 0))
        screen.blit(mines_text, (10, 40))

    # Places mines on board.
    def addMines(self, safe_rc):
        # Skip the first-clicked safe cell when placing mines
        safe_r, safe_c = safe_rc
        # Safe zone for first clicked and neighbors.
        safe_zone = set()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = safe_r + dr, safe_c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    safe_zone.add((nr, nc))
        # Randomly places mines until reaches mine count.
        placed = 0
        while placed < MINES:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            # Passes if in safe zone.
            if (r, c) in safe_zone:
                continue
            # If cell empty, place mine.
            if self.grid[r][c].cellState == 0:
                self.grid[r][c].cellState = 3  # mine
                placed += 1

    # Calls the add mine function and computes neighbors.
    def insertMines(self, safe_rc):
        # Place mines away from safe cell and compute numbers once
        self.addMines(safe_rc)
        self.compute_adjacents()
        self.minesPlaced = True

    # Reveal all mines on board
    def revealMines(self):
        # iterate through grid and for each cell if there's a mine reveal it
        for row in self.grid:
            for cell in row:
                # if cellState is a mine, reveal that cell
                if cell.cellState == 3:
                    cell.isClicked = True # reveal cell
        
    # Count adjacent mines once after placement.
    def compute_adjacents(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                # Passes on mine states.
                if cell.cellState == 3:
                    cell.adjMines = 0
                    continue
                # Counts mines around cell.
                cnt = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        # Passes on self.
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        # Checks if within bound.
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc].cellState == 3:
                                cnt += 1
                # Number of adjacent mines.
                cell.adjMines = cnt

    #Check if there are any covered left (victory)
    def victoryCheck(self):
        # Iterates through the grid and if no covered game is over with win.
        coveredcount = 0
        for row in self.grid:
            for cell in row:
                if cell.cellState == 0:
                    coveredcount += 1
        if coveredcount == 0:
            self.gameOver = True
            self.victory = True
