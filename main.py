'''
File: main.py
Authors: Jace Keagy, K Li, Ian Lim, Jenna Luong, Kit Magar, Bryce Martin.
Date: 9/10/2025
Purpose: The Entry Point and Game Loop.
External Sources: None.
'''

# Imports.
import os
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

    # Sound
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except Exception as e:
        print("Mixer init failed:", e)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    def _snd(name):
        return os.path.join(base_dir, name)

    def _load(path):
        try:
            return pygame.mixer.Sound(path)
        except Exception as e:
            print(f"Sound not loaded: {path} -> {e}")
            return None

    click_snd   = _load(_snd("audio/click.wav"))
    flag_snd    = _load(_snd("audio/flag.wav"))
    mine_snd    = _load(_snd("audio/mine.wav"))
    victory_snd = _load(_snd("audio/victory.wav"))
    lose_snd    = _load(_snd("audio/lose.wav"))

    pygame.mixer.set_num_channels(24)      
    FLAG_CH = pygame.mixer.Channel(5)      
    last_flag_ms = 0                       

    played_end  = False
    
    # Reset / Play Again UI 
    BTN_W, BTN_H = 100, 30
    BTN_MARGIN = 10
    # Button lives in the HUD (top bar)
    reset_btn_rect = pygame.Rect(330, 40, BTN_W, BTN_H)


    def draw_button(surface, rect, label):
        pygame.draw.rect(surface, (235, 235, 235), rect)     
        pygame.draw.rect(surface, (100, 100, 100), rect, 2)   
        f = pygame.font.SysFont(None, 28)
        txt = f.render(label, True, (0, 0, 0))
        surface.blit(txt, txt.get_rect(center=rect.center))

    def new_game():
        nonlocal board, input_handler, played_end
        board = Board(ROWS, COLS, mine_count)   
        input_handler = InputHandler(board)
        played_end = False


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
             # --- Keyboard: R to reset ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                 new_game()

             # --- Mouse: click Reset / Play Again button in HUD ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if my < GAME_STATE_OBJ_SIZE and reset_btn_rect.collidepoint(mx, my):
                    new_game()
                    continue  

            # Plays SFX after InputHandler updates the board
            if event.type == pygame.MOUSEBUTTONDOWN and not board.gameOver:
                mx, my = event.pos
                my_grid = my - GAME_STATE_OBJ_SIZE
                # only if click landed inside the grid, not on the HUD
                if my_grid >= 0:
                    row = my_grid // CELL_SIZE
                    col = mx // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        cell = board.grid[row][col]
                        if event.button == 1:
                            if cell.isClicked:
                                if cell.cellState == 3:
                                    if mine_snd: mine_snd.play()
                                else:
                                    if click_snd: click_snd.play()
                        elif event.button == 3:
                            # dedicated channel for right click so new play replace old ones
                            now = pygame.time.get_ticks()
                            if flag_snd and now - last_flag_ms >= 60:
                                if FLAG_CH.get_busy():
                                    FLAG_CH.stop()
                                FLAG_CH.play(flag_snd)
                                last_flag_ms = now

        screen.fill(BG_COLOR)
        board.draw(screen)

        # Checks if win, loss, or playing and blits the text.
        board.victoryCheck()

        # End of game sound effects
        if board.victory and not played_end:
            if victory_snd: victory_snd.play()
            played_end = True
        elif board.gameOver and not board.victory and not played_end:
            if lose_snd: lose_snd.play()
            played_end = True

        if board.gameOver == True and board.victory == True:
            text_rect = win_text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(win_text, text_rect)
        elif board.gameOver == True and board.victory != True:
            text_rect = lose_text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(lose_text, text_rect)
        else:
            text_rect = playing_text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(playing_text, text_rect)

        # Draw Reset / Play Again button 
        btn_label = "Play Again" if board.gameOver else "Reset (R)"
        draw_button(screen, reset_btn_rect, btn_label)

        # Display.
        pygame.display.flip()
    pygame.quit()

# Calls main function.
if __name__ == "__main__":
    main()
