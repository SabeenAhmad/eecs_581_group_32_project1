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
        print("[AI Hard] Perfect safe move placeholder")
