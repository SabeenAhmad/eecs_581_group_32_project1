import random
class AI:
    """Pure decision-making AI. It does NOT change game state; it only returns a recommended
    action for the caller to apply. This keeps game-state changes centralized in InputHandler.
    """

    def __init__(self, board, difficulty):
        self.board = board
        self.difficulty = difficulty

    def make_move(self):
        if self.board.gameOver:
            return ("none", None)
        if self.difficulty == "easy":
            return self._easy_move()
        if self.difficulty == "medium":
            return self._medium_move()
        if self.difficulty == "hard":
            return self._hard_move()
        return ("none", None)

    def _easy_move(self):
        # Collect all covered, unflagged cells
        candidates = []
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                if not cell.isClicked and not cell.isFlagged:
                    candidates.append((r, c))

        # If no candidates, do nothing
        if not candidates:
            return ("none", None)

        # Pick a random candidate
        return ("reveal", random.choice(candidates))

    def _medium_move(self):
        print("[AI Medium] Random move placeholder")

    def _hard_move(self):
        # Hard: pick a covered cell that isn't a mine
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                if not cell.isClicked and not cell.isFlagged and cell.cellState != 3:
                    return ("reveal", (r, c))
        return ("none", None)