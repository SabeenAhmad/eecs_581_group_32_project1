'''
File: main.py
Authors: Jace Keagy, K Li, Ian Lim, Jenna Luong, Kit Magar, Bryce Martin.
Date: 9/10/2025
Purpose: The Entry Point and Game Loop.
Inputs: click.wav, flag.wav, mine.wav, victory.wav, and lose.wav.
Outputs: None.
External Sources: None.
'''

# Imports.
import os
import pygame
from config import *
from board import Board
from inputHandler import InputHandler
from ai import AI

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
        # initialize pygame sound mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    # print error message
    except Exception as e:
        print("Mixer init failed:", e)

    base_dir = os.path.dirname(os.path.abspath(__file__)) # get directory of current script

    # helper func to build full paths to sound files
    def _snd(name):
        return os.path.join(base_dir, name)

    # helper func to load sound files w/ error handling
    def _load(path):
        try:
            return pygame.mixer.Sound(path)
        # print error and return None instead of crashing
        except Exception as e:
            print(f"Sound not loaded: {path} -> {e}")
            return None

    # load sound effects
    click_snd   = _load(_snd("audio/click.wav")) # click sounds
    flag_snd    = _load(_snd("audio/flag.wav")) # flag sounds
    mine_snd    = _load(_snd("audio/mine.wav")) # mine sounds
    victory_snd = _load(_snd("audio/victory.wav")) # victory sounds
    lose_snd    = _load(_snd("audio/lose.wav")) # lose sounds

    pygame.mixer.set_num_channels(24) # allows up to 24 sounds to play simultaneously
    FLAG_CH = pygame.mixer.Channel(5) # dedicated channel for flag sounds
    last_flag_ms = 0 # timestamp for flag sound cooldown
    played_end  = False # flag to track if game ended
    show_ai_popup = False #flag for showing ai mode
    # Reset / Play Again UI 
    BTN_W, BTN_H = 100, 30
    # Button lives in the HUD (top bar)
    reset_btn_rect = pygame.Rect(430, 40, BTN_W, BTN_H)

    #UI Button 
    AI_btn = pygame.Rect(10, 540, BTN_W, BTN_H)

    # func to draw button
    def draw_button(surface, rect, label):
        pygame.draw.rect(surface, (235, 235, 235), rect) # draw button's background 
        pygame.draw.rect(surface, (100, 100, 100), rect, 2) # draw dark gray border 2 pixels wide around button
        f = pygame.font.SysFont(None, 28) # create a font object w default font at size 28
        txt = f.render(label, True, (0, 0, 0)) # label text is black
        surface.blit(txt, txt.get_rect(center=rect.center)) # draw text centered within button rectangle

    # func to start a new game
    def new_game():
        nonlocal board, input_handler, played_end # access variables from outer scope
        board = Board(ROWS, COLS, mine_count) # create new game board
        input_handler = InputHandler(board) # create new input handler for the board
        played_end = False # reset end-game sound flag


    # Status text of game.
    font = pygame.font.SysFont(None, 36)
    playing_text = font.render("Playing", True, (0, 0, 0)) # text for playing
    lose_text = font.render("You Lose!", True, (0, 0, 0)) # text for losing
    win_text = font.render("You Win!", True, (0, 0, 0)) # text for winning

    # Loop that checks if game still running.
    running = True
    while running:
        # Handles user input and checks if quit.
        for event in pygame.event.get():
            response = input_handler.handle_event(event)
            if response == "quit":
                running = False # exit loop if quitting
             # --- Keyboard: R to reset ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                 new_game() # resets game

             # --- Mouse: click Reset / Play Again button in HUD ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # start new game if left-click on reset button in HUD (top area)
                if my < GAME_STATE_OBJ_SIZE and reset_btn_rect.collidepoint(mx, my):
                    new_game()
                    continue  
                # if AI button is clicked
                if AI_btn.collidepoint(mx, my):
                    show_ai_popup = not show_ai_popup  # toggle popup on/off
                    continue
                # If popup is visible, check difficulty buttons
                if easy_btn.collidepoint(mx, my):
                    ai = AI(board, "easy")
                elif medium_btn.collidepoint(mx, my):
                    ai = AI(board, "medium")
                elif hard_btn.collidepoint(mx, my):
                    ai = AI(board, "hard")

                ai.make_move()

            # Plays SFX after InputHandler updates the board
            if event.type == pygame.MOUSEBUTTONDOWN and not board.gameOver:
                mx, my = event.pos # mouse position
                my_grid = my - GAME_STATE_OBJ_SIZE # adjust Y coordinate to account for HUD height
                # only if click landed inside the grid, not on the HUD
                if my_grid >= 0:
                    row = my_grid // CELL_SIZE # row based on Y coord
                    col = mx // CELL_SIZE # col based on X coord
                    # if grid coords within bounds
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        cell = board.grid[row][col] # get cell at calculated position
                        # if left-click
                        if event.button == 1:
                            # if revealed
                            if cell.isClicked:
                                # if cell is a mine
                                if cell.cellState == 3:
                                    # play mine explosion sound if available
                                    if mine_snd: mine_snd.play()
                                # cell is not a mine
                                else:
                                    # play click sound if available
                                    if click_snd: click_snd.play()
                        # if right-click
                        elif event.button == 3:
                            # dedicated channel for right click so new play replace old ones
                            now = pygame.time.get_ticks()
                            # if flag sound exists & cooldown period passed
                            if flag_snd and now - last_flag_ms >= 60:
                                # if flag sound currently playing
                                if FLAG_CH.get_busy():
                                    FLAG_CH.stop() # stop flag sound
                                FLAG_CH.play(flag_snd) # play flag sound
                                last_flag_ms = now # update last flag sound timestamp

        # fill screen with bg color
        screen.fill(BG_COLOR)
        # draw screen
        board.draw(screen)

        # Checks if win, loss, or playing and blits the text.
        board.victoryCheck()

        # End of game sound effects
        # if player won & end sound hasn't played
        if board.victory and not played_end:
            # play victory sound
            if victory_snd: victory_snd.play()
            played_end = True # mark end sound as played
        # if player lost
        elif board.gameOver and not board.victory and not played_end:
            # play lose sound
            if lose_snd: lose_snd.play()
            played_end = True

        # if game over and player won display game status in top-right corner
        if board.gameOver == True and board.victory == True:
            text_rect = win_text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(win_text, text_rect) # win text
        
        # if game over and player lost display game status in top-right corner
        elif board.gameOver == True and board.victory != True:
            text_rect = lose_text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(lose_text, text_rect) # lose text

        # game still in progress display game status in top-right corner
        else:
            text_rect = playing_text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(playing_text, text_rect) # playing text

        # Draw Reset / Play Again button 
        btn_label = "Play Again" if board.gameOver else "Reset (R)"
        draw_button(screen, reset_btn_rect, btn_label)

        # Draw AI Button
        draw_button(screen, AI_btn, "AI Help")

        # Draw popup at bottom if enabled
        if show_ai_popup:
            popup_w, popup_h = 360, 100  
            popup_x = 20
            popup_y = HEIGHT - popup_h - 20  
            popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)

            pygame.draw.rect(screen, (240, 240, 240), popup_rect)
            pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)

            # Button dimensions
            btn_w, btn_h = 100, 40
            btn_spacing = 20
            total_width = 3 * btn_w + 2 * btn_spacing

            # Center buttons inside popup
            start_x = popup_rect.centerx - total_width // 2
            start_y = popup_rect.centery - btn_h // 2
            easy_btn   = pygame.Rect(start_x, start_y, btn_w, btn_h)
            medium_btn = pygame.Rect(start_x + btn_w + btn_spacing, start_y, btn_w, btn_h)
            hard_btn   = pygame.Rect(start_x + 2 * (btn_w + btn_spacing), start_y, btn_w, btn_h)

            draw_button(screen, easy_btn, "Easy")
            draw_button(screen, medium_btn, "Medium")
            draw_button(screen, hard_btn, "Hard")
            
        # Display.
        pygame.display.flip()
    pygame.quit()

# Calls main function.
if __name__ == "__main__":
    main()
