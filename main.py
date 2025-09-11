'''
Author: 
Date:
Purpose:
External Sources:
'''

import pygame
import random

from config import *
from board import Board

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.SysFont(None, 32)

    board = Board(ROWS, COLS)

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
                row = my // CELL_SIZE
                col = mx // CELL_SIZE
                if event.button == 1:
                    # reveal square
                    pass

                elif event.button == 3:
                    # add a flag
                    pass

        screen.fill(BG_COLOR)
        board.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
