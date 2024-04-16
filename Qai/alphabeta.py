from random import randint
from math import inf
from GUI.constants import *
from GUI.buttons import *

from Qai.player import Player

class AlphaBetaPlayer(Player):
    def __init__(self, game, max_depth=10):
        super().__init__(game)
        self.move = None
        self.max_depth = max_depth

    def __str__(self) -> str: return "Alpha Beta"

    def play(self, board) -> int | None:
        self.minimax(board, True, 0, -inf, inf)
        return self.move

    def score(self, board, max_turn, depth) -> int:
        player = -1 if max_turn else 1

        win_state = self.game.getGameEnded(board, player)
        if win_state == player:
            return 10 - depth
        elif win_state == -player:
            return depth - 10
        else:
            return 0
    
    def eval_board(self, board, max_turn) -> int:
        # filter out all completely empty lines i.e: [0, 0, 0, 0]
        state = [list(line) for line in self.returnStreaks(board) if sum(line) != 0]

        streaks = []
        blocks = []
        if max_turn:
            # [1,0,0,0] || [1,1,0,0] || [1,1,1,0] || [1,1,1,1]
            streaks = [sum(line) for line in state if sum(line) <= 4]
            # [255,255,255,1]
            blocks = [1 for line in state if sum(line) == 766 and line.count(255) == 3]
        else:
            # [255,0,0,0] || [255,255,0,0] || [255,255,255,0] || [255,255,255,255]
            streaks = [line.count(255) for line in state if sum(line) % 255 == 0]
            # [1,1,1,255]
            blocks = [1 for line in state if sum(line) == 766 and line.count(1) == 3]


        streak_score = self.attributes['in-a-row'] * len(streaks) + self.attributes['per-streak'] * sum(streaks)
        block_score = self.attributes['total-block'] * len(blocks)
        return int(streak_score + block_score)
        streaks = self.returnStreaks(board)
        points_max = 0
        points_min = 0
        for streak in streaks:
            streak_sum = sum(streak)

            if streak_sum < 4:
                points_max += streak_sum if max_turn else int(streak_sum / 2)

            if streak_sum > 510:
                points_min += 1
            elif streak_sum > 255:
                points_min += 2
            elif streak_sum > 200:
                points_min += 3

        num1 = randint(-10, 10)
        num2 = randint(-10, 10)
        scale = 0
        if max_turn:
            scale = max(num1, num2)
            return (scale * points_max) - (10 * points_min)
        else:
            scale = min(num1, num2)
            return (scale * points_min) - (10 * points_max)

    
    def minimax(self, board, max_turn, depth, alpha, beta) -> int:
        player = -1 if max_turn else 1
        if self.game.getGameEnded(board, player) != 0:
            return self.score(board, max_turn, depth)
        
        if depth >= self.max_depth:
            return self.eval_board(board, max_turn)
        
        depth += 1
        scores = []
        moves = []

        empty_cells = [i for (i, valid) in enumerate(self.game.getValidMoves(board, 1)) if valid]

        # best_score = -inf if max_turn else inf
        # best_idx = 0
        for idx, move in enumerate(empty_cells):
            curr_board, _ = self.game.getNextState(board, player, move)
            curr_score = self.minimax(curr_board, (not max_turn), depth, alpha, beta)
            scores.append(curr_score)
            moves.append(move)

            if max_turn:
                alpha = max(alpha, curr_score)
            else:
                beta = min(beta, curr_score)
            if beta <= alpha:
                break

        if max_turn:
            index_max = max(range(len(scores)), key=scores.__getitem__)
            self.move = moves[index_max]
            return scores[index_max]
        else:
            index_min = min(range(len(scores)), key=scores.__getitem__)
            self.move = moves[index_min]
            return scores[index_min]