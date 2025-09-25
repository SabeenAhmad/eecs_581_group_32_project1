'''
File: inputHandler.py
Authors: Jace Keagy, K Li, Ian Lim, Jenna Luong, Kit Magar, Bryce Martin.
Date: 9/15/2025
Purpose: Input handler for user clicks. Handles input for Minesweeper.
Inputs: None.
Outputs: None.
External Sources: None.
'''

# Imports.
import pygame
from config import *

# Handles input of user.
class InputHandler:
    def __init__(self, board):
        # References board and tracks if first cell clicked.
        self.board = board
        self.firstClick = True

    def reveal_cell(self, row, col):
        """Centralized reveal logic used by both human input and AI decisions.
        """
        # bounds check
        if not (0 <= row < ROWS and 0 <= col < COLS):
            return False
        cell = self.board.grid[row][col]
        if cell.isFlagged or cell.isClicked:
            return False
        # First click flow: place mines safely around (row,col)
        if self.firstClick:
            cell.cellState = 2
            self.firstClick = False
            self.board.insertMines((row, col))
            cell.revealGrid(self.board.grid)
        else:
            cell.revealGrid(self.board.grid)
        cell.isClicked = True
        if cell.cellState == 3:
            self.board.gameOver = True
            self.board.revealMines()
        return True

    # Handles each input event.
    def handle_event(self, event):
        # Check if user exits.
        if event.type == pygame.QUIT:
            return "quit"
        # Check if left mouse button pressed & game is not over.
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.board.gameOver:
            # X & Y coordinates of mouse.
            mx, my = event.pos
            # Adjustment for top bar.
            my_grid = my - GAME_STATE_OBJ_SIZE
            if my_grid < 0:
                return
            # Transistion to cell coordinates.
            row = my_grid // CELL_SIZE
            col = mx // CELL_SIZE
            # Ignores out of bounds clicks.
            if not (0 <= row < ROWS and 0 <= col < COLS):
                return
            # Identifies cell.
            cell = self.board.grid[row][col]
            # Uncover cell button.
            if event.button == 1:
                # Makes sure cell isn't flagged and then mark as clicked.
                if not cell.isFlagged:
                    # Delegate to centralized reveal logic
                    revealed = self.reveal_cell(row, col)
                    if revealed:
                        return "revealed"
            # Right click toggles flag if cell not uncovered.
            elif event.button == 3:
                if not cell.isClicked:
                    cell.isFlagged = not cell.isFlagged
