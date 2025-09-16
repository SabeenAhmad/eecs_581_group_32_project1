'''
Author: Bryce Martin
Date: 09-15-2025
Purpose: Handle All User Inputs
External Sources:
'''

import pygame
from config import *

class InputHandler:
    def __init__(self, board):
        self.board = board
        self.firstClick = True

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return "quit"
        # check if mouse button pressed & game is not over
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.board.gameOver:
            # x & y coordinates of mouse
            mx, my = event.pos
            my_grid = my - GAME_STATE_OBJ_SIZE
            if my_grid < 0:
                return
            row = my_grid // CELL_SIZE
            col = mx // CELL_SIZE
            if not (0 <= row < ROWS and 0 <= col < COLS):
                return
            cell = self.board.grid[row][col]
            if event.button == 1:
                if not cell.isFlagged:
                    #If first clicked, mark as uncovered then add the mines.
                    if self.firstClick == True:
                        cell.cellState = 2
                        self.firstClick = False
                        self.board.insertMines((row,col))
                        cell.revealGrid(self.board.grid)
                    else:
                        # Updated by Kit — 2025-09-15: reveal using flood-fill so zeros expand
                        cell.revealGrid(self.board.grid)
                    cell.isClicked = True
                    # if mine is clicked, game over
                    if cell.cellState == 3:
                        self.board.gameOver = True
                        self.board.revealMines() # updated by Jenna - reveal all mines once game is over
            elif event.button == 3:
                if not cell.isClicked:
                    cell.isFlagged = not cell.isFlagged