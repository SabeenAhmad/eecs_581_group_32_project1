'''
Author: K Li
Date: 2025-09-11
Update: Added UI drawing for flags, mines, and numbers
Purpose: Cell class with rendering logic for Minesweeper
External Sources: N/A
'''

# Cell Definition

import pygame
from config import *

class Cell:
    def __init__(self, row, col, cellState):
        self.row = row # y pos of grid
        self.rowSize = row * CELL_SIZE # size of row, height of grid
        self.col = col # x pos of grid
        self.colSize = col * CELL_SIZE # size of col, width of grid
        self.cellState = cellState # state of cell, 3 is mine
        self.isClicked = False # bool to check if cell is clicked
        self.isFlagged = False # bool to check if cell flagged
        self.adjMines = 0 # var to count adjacent mines
    
    # Updated by K Li on 2025-09-11
    # Added number rendering (colored text), mine (circle), and flag (triangle)
    def rect(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    def draw(self, gridSurface):
        # Updated by Kit — 2025-09-15: correct x/y from col/row (fix click/draw alignment)
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        #$Create a rectangle for this cell based on its position    

        # Default rendering for a covered cell
        pygame.draw.rect(gridSurface, GRID_COLOR, rect)
        pygame.draw.rect(gridSurface, BORDER_COLOR, rect, 1)

        if self.isClicked:
            # If the cell has been revealed
            pygame.draw.rect(gridSurface, REVEALED_BG, rect)
            pygame.draw.rect(gridSurface, BORDER_COLOR, rect, 1)

            if self.cellState == 3:
                # Draw a mine as a black circle if this cell is a mine
                pygame.draw.circle(gridSurface, MINE_COLOR, rect.center, CELL_SIZE // 4)
            elif self.adjMines > 0:
                self.cellState = 2 # Updates cell state
                # Draw the number of adjacent mines with the proper color
                color = NUMBER_COLORS.get(self.adjMines, TEXT_COLOR)
                font = pygame.font.SysFont(None, 24)
                num_surface = font.render(str(self.adjMines), True, color)
                num_rect = num_surface.get_rect(center=rect.center)
                gridSurface.blit(num_surface, num_rect)
            # If adjMines == 0, leave it as an empty revealed cell
        else:
            # If the cell is still covered, show a flag if it is flagged
            if self.isFlagged:
                pole_x = rect.x + CELL_SIZE // 3
                # Draw the flag pole
                pygame.draw.line(gridSurface, (80, 80, 80),
                                (pole_x, rect.y + CELL_SIZE // 4),
                                (pole_x, rect.y + 3 * CELL_SIZE // 4), 2)
                # Draw the triangular red flag
                flag_pts = [
                    (pole_x, rect.y + CELL_SIZE // 4),
                    (pole_x + CELL_SIZE // 2, rect.y + CELL_SIZE // 3),
                    (pole_x, rect.y + CELL_SIZE // 2)
                ]
                pygame.draw.polygon(gridSurface, FLAG_COLOR, flag_pts)
    
    # updated by Jenna Luong 9/13/25
    # recursively reveals grid
    # Updated by Kit — 2025-09-15: When a cell with 0 adjacent mines is clicked it needs to reveal all touching 0-cells.
    def revealGrid(self, grid):
        # Skip if this cell is already opened or flagged
        if self.isClicked or self.isFlagged:
            return

        # reveal cell
        self.isClicked = True

        #Updates cell state
        if self.cellState == 0:
            self.cellState = 2

        # if mine is clicked reveal all mines (game over)
        # Updated by Kit — 2025-09-15: early return on mine; Board handles revealing all mines
        if self.cellState == 3:  
            return

        # Kit — Reveal neighbors when there are no adjacent mines.
        if self.adjMines == 0:
            rows = len(grid)
            cols = len(grid[0]) if rows > 0 else 0

            # check all 8 adj cells
            # Updated by Kit — 2025-09-15: compute neighbor coords INSIDE the inner loop so flood-fill expands
            for r in range(-1, 2):
                for c in range(-1, 2):
                    if r == 0 and c == 0:
                        continue  # skip current cell

                    new_row = self.row + r          # Updated by Kit — 2025-09-15
                    new_col = self.col + c          # Updated by Kit — 2025-09-15

                    # check if adj cell within cell bounds
                    if 0 <= new_row < rows and 0 <= new_col < cols:
                        adjCell = grid[new_row][new_col]
                        if not adjCell.isClicked and not adjCell.isFlagged:
                            adjCell.revealGrid(grid)


