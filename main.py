'''
Author: 
Date:
Purpose:
External Sources:
'''
import numpy as np
import pygame
from config import *
from board import Board

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.SysFont(None, 32)
    board = Board(ROWS, COLS)
    firstClick = True #Checks if is first click
    running = True
    while running:
        # user input
        for event in pygame.event.get():
            # check if the player closed the window
            if event.type == pygame.QUIT:
                running = False # exit loop
            # check if mouse button pressed & game is not over
            elif event.type == pygame.MOUSEBUTTONDOWN and not board.gameOver:
                # x & y coordinates of mouse
                mx, my = event.pos
                my_grid = my - GAME_STATE_OBJ_SIZE
                if my_grid < 0:
                    continue  
                row = my_grid // CELL_SIZE
                col = mx // CELL_SIZE
                if not (0 <= row < ROWS and 0 <= col < COLS):
                    continue
                cell = board.grid[row][col]
                if event.button == 1:
                    if not cell.isFlagged:
                        cell.isClicked = True
                        #If first clicked, mark as uncovered then add the mines.
                        if firstClick == True:
                            cell.cellState = 2
                            firstClick = False
                            board.insertMines((row,col))
                        # Updated by Kit — 2025-09-15: reveal using flood-fill so zeros expand
                        cell.revealGrid(board.grid)
                        if cell.cellState == 3:
                            board.gameOver = True
                elif event.button == 3:
                    if not cell.isClicked:
                        cell.isFlagged = not cell.isFlagged
        screen.fill(BG_COLOR)
        board.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
