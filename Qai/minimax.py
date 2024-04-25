from GUI.constants import *
from GUI.buttons import *

from Qai.player import Player
from Qai.streaks import returnStreaks

class MiniMaxPlayer(Player):
    def __init__(self, game, vs_ai, max_depth=10):
        super().__init__(game)
        self.move = None
        self.max_depth = max_depth
        self.vs_ai = vs_ai

    def __str__(self) -> str:
        return "Mini Max"

    def play(self, board) -> int | None:
        self.move = None
        self.minimax(board, True)
        return self.move


    def score(self, board, max_turn, depth):
        player = -1 if max_turn else 1

        win_state = self.game.getGameEnded(board, player)
        if win_state == player:
            return 10 - depth
        elif win_state == -player:
            return depth - 10
        else:
            return 0

    def eval_board(self, board, max_turn):
        # filter out all completely empty lines i.e: [0, 0, 0, 0]
        state = [list(line) for line in returnStreaks(board) if sum(line) != 0]

        streaks = []
        blocks = []
        # [1,0,0,0] || [1,1,0,0] || [1,1,1,0] || [1,1,1,1]
        streaks = [sum(line) for line in state if sum(line) <= 4]
        # [255,255,255,1]
        blocks = [1 for line in state if sum(line) == 766 and line.count(255) == 3]

        streak_score = self.attributes['in-a-row'] * len(streaks) + self.attributes['per-streak'] * sum(streaks)
        block_score = self.attributes['total-block'] * len(blocks)

        if max_turn:
            return int(streak_score + block_score)
        else:
            return int(streak_score - block_score)

    def minimax(self, board, max_turn, depth=0):
        player = -1 if max_turn else 1
        if self.game.getGameEnded(board, player) != 0:
            return self.score(board, max_turn, depth)

        if depth >= self.max_depth:
            return self.eval_board(board, max_turn)

        depth += 1
        scores = []
        moves = []

        empty_cells = [i for (i, valid) in enumerate(self.game.getValidMoves(self.game.getCanonicalForm(board, player), 1)) if valid]
        for move in empty_cells:
            curr_board, _ = self.game.getNextState(self.game.getCanonicalForm(board, player), player, move)
            if self.vs_ai:
                curr_score = self.minimax(self.game.getCanonicalForm(curr_board, player), (not max_turn), depth)
            else:
                curr_score = self.minimax(curr_board, (not max_turn), depth)
            scores.append(curr_score)
            moves.append(move)

        if max_turn:
            index_max = max(range(len(scores)), key=scores.__getitem__)
            self.move = moves[index_max]
            return scores[index_max]
        else:
            index_min = min(range(len(scores)), key=scores.__getitem__)
            self.move = moves[index_min]
            return scores[index_min]