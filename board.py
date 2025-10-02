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
        self.best_time_seconds = None     #filled later by timer logic
        self.best_time_holder = None      #name tied to best time

    def set_player_name(self, name: str):
        self.player_name = name if name else "Player"

    # Calculate flag count by subtracting flags from mines
    def flag_count(self):
        flags = sum(cell.isFlagged for row in self.grid for cell in row)
        return max(self.mine_count - flags, 0)
    def update_high_score(self, player_name, elapsed_time):
        if elapsed_time is None:
            return
        if self.best_time_seconds is None or elapsed_time < self.best_time_seconds:
            self.best_time_seconds = elapsed_time
            self.best_time_holder = player_name

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

        # Render the elapsed game time
        # Anna needs to add timer logic so we can add a variable to the following line of code to get time to actually appear.
        # game_time_text = font.render(f"Game time: ", True, (0, 0, 0))
        # screen.blit(game_time_text, (10, 560))

        # Render the high score (longest elapsed game time)
        # Sriya needs to ask for player name in main.py
        # high_score_text = font.render(f"High score: (Achieved by: {self.player_name})" , True, (0, 0, 0))
        # screen.blit(high_score_text, (10, 590))

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

        #player & future timer/highscore
        footer_font = pygame.font.SysFont(None, 28)
        # --- Footer: one-line status ---
        footer_y = HEIGHT - EXTRA_HEIGHT + 10

        # Build labels
        timer_label = "--"  # replace later with real timer
        hs_label = "--"
        if self.best_time_seconds is not None and self.best_time_holder:
            m, s = divmod(int(self.best_time_seconds), 60)
            hs_label = f"{m:02d}:{s:02d} by {self.best_time_holder}"

        line = f"Player: {self.player_name}   Time: {timer_label}   High score: {hs_label}"

        # Fit-to-width: try smaller fonts if needed
        for size in (28, 24, 20, 18):
            footer_font = pygame.font.SysFont(None, size)
            line_surf = footer_font.render(line, True, (0, 0, 0))
            if line_surf.get_width() <= WIDTH - 20:
                break

        screen.blit(line_surf, (10, footer_y))


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
