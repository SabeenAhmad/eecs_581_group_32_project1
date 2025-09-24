class AI:
    def __init__(self, board, difficulty):
        self.board = board
        self.difficulty = difficulty

    def make_move(self):
        """Decide and play a move based on difficulty."""
        if self.difficulty == "easy":
            return self._easy_move()
        elif self.difficulty == "medium":
            return self._medium_move()
        elif self.difficulty == "hard":
            return self._hard_move()

    def _easy_move(self):
        print("[AI Easy] Random move placeholder")

    def _medium_move(self):
        print("[AI Medium] Strategic move placeholder")

    def _hard_move(self):
        """Cheating AI: always pick a guaranteed safe cell. It scans the board for any covered cell that is not a mine based
        on the board's internal state. If no safe covered cells are left, returns none.
        """
        # Use full knowledge of cell.cellState == 3 to avoid mines
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                if not cell.isClicked and not cell.isFlagged and cell.cellState != 3:
                    # reveal this safe cell
                    if hasattr(self.board, 'minesPlaced') and not getattr(self.board, 'minesPlaced'):
                        cell.cellState = 2
                        self.board.insertMines((r, c))
                        cell.revealGrid(self.board.grid)
                    else:
                        cell.revealGrid(self.board.grid)
                        cell.isClicked = True
                    # signal move
                    return ("reveal", (r, c))
        return ("none", None)

