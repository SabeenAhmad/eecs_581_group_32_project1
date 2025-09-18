'''
File: main.py
Authors: Jace Keagy, K Li, Ian Lim, Jenna Luong, Kit Magar, Bryce Martin.
Date: 9/10/2025
Purpose: The Entry Point and Game Loop.
External Sources: None.
'''

# Imports.
import pygame
from config import *
from board import Board
from inputHandler import InputHandler

# function to get # mines from user
def mine_input():
    # loop
    while True:
        try:
            # get user input
            user_input = input("Enter the number of mines (10-20): ")
            mine_count = int(user_input) # mine count is the int of the user input
            # if mine count not 10 to 20, print
            if mine_count < 10 or mine_count > 20:
                print("Please enter a number between 10 and 20.")
            # mine count 10-20
            else:
                return mine_count
        # print exception
        except ValueError:
            print("Please enter a valid number.\n")

# Main function.
def main():
    # get count of mines
    mine_count = mine_input()
    # Sets up PyGame and the board.
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    board = Board(ROWS, COLS, mine_count)
    input_handler = InputHandler(board)
    # Status text of game.
    font = pygame.font.SysFont(None, 36)
    playing_text = font.render("Playing", True, (0, 0, 0))
    lose_text = font.render("You Lose!", True, (0, 0, 0))
    win_text = font.render("You Win!", True, (0, 0, 0))
    # Loop that checks if game still running.
    running = True
    while running:
        # Handles user input and checks if quit.
        for event in pygame.event.get():
            response = input_handler.handle_event(event)
            if response == "quit":
                running = False
        screen.fill(BG_COLOR)
        board.draw(screen)
        # Checks if win, loss, or playing and blits the text.
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
        # Display.
        pygame.display.flip()
    pygame.quit()

# Calls main function.
if __name__ == "__main__":
    main()
