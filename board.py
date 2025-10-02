'''
File: board.py
Authors: Jace Keagy, K Li, Ian Lim, Jenna Luong, Kit Magar, Bryce Martin.
Date: 9/10/25
Purpose: Create & manage 2D grid, insert mines, compute adjacent mines, 
calculates mines left, check if victory.
Inputs: None.
Outputs: None.
External Sources: None.
'''

# Imports.
import random
from cell import Cell
from config import *
import pygame
import time
# Class for handing the board.
class Board:
    def __init__(self, rows, cols, mine_count, ai_mode, difficulty):
        self.rows = rows # number of rows
        self.cols = cols # number of cols
        self.mine_count = mine_count # mine count
        self.difficulty = difficulty
        self.ai_mode = ai_mode
        self.GRID_TOP_MARGIN = 50   # space in pixels for text/UI above grid
        self.gridSurface = pygame.Surface((WIDTH, HEIGHT - GAME_STATE_OBJ_SIZE)) # grid surface with PyGame
        self.grid = [[Cell(r, c, 0) for c in range(cols)] for r in range(rows)] # Fills grid with proper row and col count with '0' cell state.
        self.gameOver = False # bool to check if game over (mine clicked on grid)
        self.victory = False # bool to check if won
        self.player_name = "Player"
        self.best_time_seconds = None # used for high score   
        self.best_time_holder = None # name tied to best time
        self.start_time = None # used for timer
        self.elapsed_time_seconds = 0 # value of timer

    def set_player_name(self, name: str):
        self.player_name = name if name else "Player"

    # Calculate flag count by subtracting flags from mines
    def flag_count(self):
        flags = sum(cell.isFlagged for row in self.grid for cell in row)
        return max(self.mine_count - flags, 0)
        
    # Draws the board.
    def draw(self, screen):
        # Clear once per frame (moved out of the loop)
        self.gridSurface.fill((210, 210, 210))
        for row in self.grid:
            for cell in row:
                cell.draw(self.gridSurface)
        screen.blit(self.gridSurface, (0, GAME_STATE_OBJ_SIZE + self.GRID_TOP_MARGIN))
        # Renders how many flags are placed.
        font = pygame.font.SysFont(None, 36)
        flags_text = font.render(f"Flag count: {self.flag_count()}", True, (0, 0, 0))
        screen.blit(flags_text, (10, 10))

        # Render how many mines there are total
        mines_text = font.render(f"Mine count: {self.mine_count}", True, (0, 0, 0))
        screen.blit(mines_text, (10, 40))

        # Render how the AI difficulty
        if self.ai_mode == "y":     
            if self.difficulty in ["easy", "medium", "hard"]:
                mines_text = font.render(f"AI difficulty: {self.difficulty}", True, (0, 0, 0))        
        else:
            mines_text = font.render(f"AI mode disabled", True, (0, 0, 0))  
        screen.blit(mines_text, (10, 70))

        # Render labels for columns
        for c in range(self.cols):
            colLabel = font.render(chr(65 + c), True, TEXT_COLOR)
            screen.blit(colLabel, (c * CELL_SIZE + 10, (GAME_STATE_OBJ_SIZE + self.GRID_TOP_MARGIN)-(CELL_SIZE/2) - 10))

        # Render labels for rows
        for r in range(self.rows):
            rowLabel = font.render(str(r + 1), True, TEXT_COLOR)
            grid_right_edge = COLS * CELL_SIZE   # end of grid
            label_x = grid_right_edge + 10       # row numbers appear right after grid
            label_y = (GAME_STATE_OBJ_SIZE + self.GRID_TOP_MARGIN) + (r * CELL_SIZE) + 10
            screen.blit(rowLabel, (label_x, label_y))
        
        # Render high scorer for the difficulty being played
        if self.best_time_seconds and self.best_time_holder: # if there is an available high score
            font = pygame.font.SysFont(None, 36)
            txt = font.render(
                f"Best: {self.best_time_holder} - {self.best_time_seconds:.2f}s",
                True,
                (0, 0, 0)
            )
            screen.blit(txt, (10, 560))  
        else: # if there is no high score for that difficulty --> None
            font = pygame.font.SysFont(None, 36)
            txt = font.render("Highest Score: None", True, (0, 0, 0))
            screen.blit(txt, (10, 560))

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
        while placed < self.mine_count:
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

    # Functions used to render the elapsed game time
    def start_timer(self):
        self.start_time = time.time() # current time

    def update_timer(self):
        if self.start_time is not None and not self.gameOver:
            self.elapsed_time_seconds = time.time() - self.start_time # updating timer

    def stop_timer(self):
        if self.start_time is not None:
            self.elapsed_time_seconds = time.time() - self.start_time # total timer
            self.start_time = None  
