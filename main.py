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
    ai_mode = input("Do you want to enable AI mode? (y/n): ").strip().lower()
    if ai_mode == 'y':
        difficulty = input("Select AI difficulty (easy, medium, hard): ").strip().lower()
        if difficulty in ["easy", "medium", "hard"]:
            print(f"AI mode enabled with {difficulty} difficulty.")
        else:
            print("Invalid difficulty. AI mode disabled.")
    else:
        difficulty = []
        print("AI mode disabled.")
    # Sets up PyGame and the board.
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    board = Board(ROWS, COLS, mine_count, ai_mode, difficulty)
    input_handler = InputHandler(board)
    # AI state for scheduled moves
    ai = None
    ai_pending = None
    ai_waiting = False
    ai_wait_start = 0
    ai_wait_duration = 1000  #1 second
    # track who made the last move: 'human' or 'ai' (used for end-of-game messaging)
    last_mover = None

    # If user opted into AI mode at startup, create AI instance now
    if ai_mode == 'y' and difficulty in ["easy", "medium", "hard"]:
        ai = AI(board, difficulty)

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
    # Reset / Play Again UI 
    BTN_W, BTN_H = 100, 30
    # Button lives in the HUD (top bar)
    reset_btn_rect = pygame.Rect(430, 40, BTN_W, BTN_H)

    #UI Button 
    # (AI popup/button removed; AI enabled via startup prompt)

    # func to draw button
    def draw_button(surface, rect, label):
        pygame.draw.rect(surface, (235, 235, 235), rect) # draw button's background 
        pygame.draw.rect(surface, (100, 100, 100), rect, 2) # draw dark gray border 2 pixels wide around button
        f = pygame.font.SysFont(None, 28) # create a font object w default font at size 28
        txt = f.render(label, True, (0, 0, 0)) # label text is black
        surface.blit(txt, txt.get_rect(center=rect.center)) # draw text centered within button rectangle

    # func to start a new game
    def new_game():
        nonlocal board, input_handler, played_end, ai, ai_pending, ai_waiting, last_mover
        # recreate board and handler
        board = Board(ROWS, COLS, mine_count, ai_mode, difficulty)
        input_handler = InputHandler(board)
        played_end = False
        # reset any scheduled AI state
        ai_pending = None
        ai_waiting = False
        last_mover = None
        # if AI mode was enabled at startup, recreate AI tied to the new board
        if ai_mode == 'y' and difficulty in ["easy", "medium", "hard"]:
            ai = AI(board, difficulty)
        else:
            ai = None


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
            # Always allow quitting and reset key even while AI is thinking
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                new_game()
                continue

            # Block mouse clicks while AI is thinking
            if ai_waiting and event.type == pygame.MOUSEBUTTONDOWN:
                # still allow quitting and reset (handled above); otherwise ignore input
                continue

            # Let InputHandler handle the event (includes left-click reveal / right-click flag)
            response = input_handler.handle_event(event)
            if response == "quit":
                running = False
                break
            # If a human revealed a cell, schedule AI to move (if AI is enabled)
            if response == "revealed":
                # human made a reveal
                last_mover = 'human'
                # schedule AI only if AI is enabled
                if ai is not None and not board.gameOver:
                    ai_pending = ai.make_move()
                    if ai_pending and ai_pending[0] != "none":
                        ai_waiting = True
                        ai_wait_start = pygame.time.get_ticks()

            # --- Mouse: click Reset / Play Again button in HUD ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # start new game if left-click on reset button in HUD (top area)
                if my < GAME_STATE_OBJ_SIZE and reset_btn_rect.collidepoint(mx, my):
                    new_game()
                    continue  
                # AI popup/button removed — AI controlled via startup prompt

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

        # If AI is waiting and duration elapsed, perform AI move
        if ai_waiting and ai_pending and not board.gameOver:
            now = pygame.time.get_ticks()
            if now - ai_wait_start >= ai_wait_duration:
                action, rc = ai_pending
                if action == "reveal" and rc is not None:
                    r, c = rc
                    # AI is about to act
                    last_mover = 'ai'
                    input_handler.reveal_cell(r, c)
                ai_pending = None
                ai_waiting = False

        # fill screen with bg color
        screen.fill(BG_COLOR)
        # draw screen
        board.draw(screen)

        # Checks if win, loss, or playing and blits the text.
        board.victoryCheck()

        # AI thinking indicator (red) while waiting - bottom center
        if ai_waiting:
            f_small = pygame.font.SysFont(None, 28)
            txt = f_small.render("AI thinking...", True, (200, 0, 0))
            tw, th = txt.get_size()
            x = (WIDTH - tw) // 2
            y = HEIGHT - th - 20
            screen.blit(txt, (x, y))

        # End of game sound effects and messages
        if board.victory and not played_end:
            # Someone won. If last mover was AI, say AI won; otherwise user won.
            if last_mover == 'ai':
                # AI won
                if lose_snd: lose_snd.play()
            else:
                # human won
                if victory_snd: victory_snd.play()
            played_end = True
        elif board.gameOver and not board.victory and not played_end:
            # Game over due to a mine. If AI caused the gameOver, the human wins; if human caused it, human loses.
            if last_mover == 'ai':
                # AI clicked a mine -> human wins
                if victory_snd: victory_snd.play()
            else:
                # human clicked a mine -> human loses
                if lose_snd: lose_snd.play()
            played_end = True

        # End-game UI messaging (top-right)
        if board.victory:
            if last_mover == 'ai':
                txt = font.render("AI won!", True, (0, 0, 0))
            else:
                txt = font.render("You Win!", True, (0, 0, 0))
            screen.blit(txt, txt.get_rect(topright=(WIDTH - 10, 10)))
        elif board.gameOver and not board.victory:
            # If AI triggered the mine, that's a human win; otherwise human lose
            if last_mover == 'ai':
                txt = font.render("You Win!", True, (0, 0, 0))
            else:
                txt = font.render("You Lose!", True, (0, 0, 0))
            screen.blit(txt, txt.get_rect(topright=(WIDTH - 10, 10)))
        else:
            screen.blit(playing_text, playing_text.get_rect(topright=(WIDTH - 10, 10)))

        # Draw Reset / Play Again button 
        btn_label = "Play Again" if board.gameOver else "Reset (R)"
        draw_button(screen, reset_btn_rect, btn_label)

        # AI UI removed (AI enabled through startup prompt)
        # Display.
        pygame.display.flip()
    pygame.quit()

# Calls main function.
if __name__ == "__main__":
    main()
