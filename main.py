'''
Author: Bryce Martin
Date: 09-10-2025
Purpose: The Entry Point and Game Loop
External Sources:
'''

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

    font = pygame.font.SysFont(None, 36)
    playing_text = font.render("Playing", True, (0, 0, 0))
    lose_text = font.render("You Lose!", True, (0, 0, 0))
    win_text = font.render("You Win!", True, (0, 0, 0))
    
    running = True
    while running:
        # user input
        for event in pygame.event.get():
            response = input_handler.handle_event(event)
            if response == "quit":
                running = False
        screen.fill(BG_COLOR)
        board.draw(screen)

        board.victoryCheck()
        if board.gameOver == True and board.victory == True:
            text_rect = win_text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(win_text, text_rect)
        elif board.gameOver == True and board.victory != True:
            text_rect = lose_text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(lose_text, text_rect)
        else:
            text_rect = playing_text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(playing_text, text_rect)

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
