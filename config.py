'''
File: config.py
Authors: Jace Keagy, K Li, Ian Lim, Jenna Luong, Kit Magar, Bryce Martin.
Date: 9/11/2025
Purpose: Config file for Minesweeper containing colors and board information.
External Sources: None.
'''

# Config
ROWS = 10 
COLS = 10
MINES = 15 # 10-20
CELL_SIZE = 40
GAME_STATE_OBJ_SIZE = 100
COL_LABEL_SIZE = 40
WIDTH = COLS * CELL_SIZE + COL_LABEL_SIZE
HEIGHT = ROWS * CELL_SIZE + GAME_STATE_OBJ_SIZE

# Colors
BG_COLOR = (220, 220, 220)
GRID_COLOR = (180, 180, 180)
TEXT_COLOR = (50, 50, 50)
REVEALED_BG = (200, 200, 200)
BORDER_COLOR = (100, 100, 100)
FLAG_COLOR = (220, 0, 0)
MINE_COLOR = (0, 0, 0)

# Added UI colors (numbers, revealed cells, flags, mines)
NUMBER_COLORS = {
    1: (25, 118, 210),   # blue
    2: (56, 142, 60),    # green
    3: (211, 47, 47),    # red
    4: (123, 31, 162),   # purple
    5: (244, 81, 30),    # orange
    6: (0, 121, 107),    # teal
    7: (66, 66, 66),     # dark gray
    8: (33, 33, 33)      # black
}