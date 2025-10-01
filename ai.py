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
        # Check if any zero-mine cells have been revealed to trigger strategic mode
        has_zero_revealed = any(
            cell.isClicked and cell.adjMines == 0 
            for row in self.board.grid for cell in row
        )
        
        # If zero-mine cell revealed, use logical deduction
        if has_zero_revealed:
            safe_move = self._find_safe_move()
            if safe_move:
                return ("reveal", safe_move)
        
        # Make random moves initially or fall back to random
        candidates = []
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                if not cell.isClicked and not cell.isFlagged:
                    candidates.append((r, c))
        
        if candidates:
            return ("reveal", random.choice(candidates))
        return ("none", None)

    def _find_safe_move(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                if cell.isClicked and cell.adjMines > 0:
                    neighbors = self._get_neighbors(r, c)
                    covered = [pos for pos in neighbors if not self.board.grid[pos[0]][pos[1]].isClicked and not self.board.grid[pos[0]][pos[1]].isFlagged]
                    flagged = [pos for pos in neighbors if self.board.grid[pos[0]][pos[1]].isFlagged]
                    
                    if len(flagged) == cell.adjMines and covered:
                        return covered[0]
        return None

    def _get_neighbors(self, r, c):
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.board.rows and 0 <= nc < self.board.cols:
                    neighbors.append((nr, nc))
        return neighbors


    def _hard_move(self):
        # Hard: pick a random covered cell that isn't a mine 
        safe_cells = []
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                if not cell.isClicked and not cell.isFlagged and cell.cellState != 3:
                    safe_cells.append((r, c))
        if safe_cells:
            choice = random.choice(safe_cells)
            return ("reveal", choice)
        return ("none", None)