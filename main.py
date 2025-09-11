import pygame

from config import *
from board import Board

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.SysFont(None, 32)

    board = Board(ROWS, COLS, MINES)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not board.gameOver:
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
        board.draw(screen, font)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
