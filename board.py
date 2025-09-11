# Board definition

from cell import Cell

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.minesCount = mines
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.gameOver = False
        self.victory = False

    def draw(self, screen, font):
        for row in self.grid:
            for cell in row:
                cell.draw(screen, font)