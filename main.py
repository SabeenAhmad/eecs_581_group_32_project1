'''
Author: Bryce Martin
Date: 09-10-2025
Purpose: The Entry Point and Game Loop
External Sources:
'''

import numpy as np
import pygame
from config import *
from board import Board
from inputHandler import InputHandler

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")

    board = Board(ROWS, COLS)
    input_handler = InputHandler(board)
    
    running = True
    while running:
        # user input
        for event in pygame.event.get():
            response = input_handler.handle_event(event)
            if response == "quit":
                running = False
            
        screen.fill(BG_COLOR)
        board.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
