from random import randint
from math import inf
from GUI.constants import *
from GUI.buttons import *

from Qai.player import Player

import threading

class MiniMaxPlayer(Player):
    def __init__(self, game, max_depth=10):
        super().__init__(game)
        self.move = None
        self.max_depth = max_depth

        self.mutex_locked = False
        
    def play(self, board) -> int | None:
        if not self.mutex_locked:
            thread_worker = threading.Thread(target=self.minimax, args=(board, True,))
            thread_worker.start()
            self.mutex_locked = True
        else:
            if thread_worker.is_alive():
                return None
            
            return self.move

        # self.minimax(board, True)
        # return self.move

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


    
    def minimax(self, board, max_turn, depth=0):
        player = -1 if max_turn else 1
        if self.game.getGameEnded(board, player) != 0:
            return self.score(board, max_turn, depth)
        
        if depth >= self.max_depth:
            return self.eval_board(board, max_turn)
        
        depth += 1
        scores = []
        moves = []

        empty_cells = [i for (i, valid) in enumerate(self.game.getValidMoves(board, 1)) if valid]
        for move in empty_cells:
            curr_board, _ = self.game.getNextState(board, player, move)
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