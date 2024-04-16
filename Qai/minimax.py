from random import randint
from math import inf
import time
from GUI.constants import *
from GUI.buttons import *

from Qai.player import Player

class MiniMaxPlayer(Player):
    def __init__(self, game, player, max_depth=10):
        super().__init__(game)
        self.move = None
        self.max_depth = max_depth
        self.player = player    
    def __str__(self) -> str: return "Mini Max"

    def play(self, board) -> int | None:
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
        
    def get_streaks(self, board):
        if self.player == 1:
            return self.returnStreaks(board)
        else:
            opp_board = []
            for line in self.returnStreaks(board):
                opp_line = []
                for x in line:
                    if x == 1:
                        opp_line.append(255)
                    elif x == 255:
                        opp_line.append(1)
                    else:
                        opp_line.append(0)
                opp_board.append(opp_line)
            
            return opp_board

    def eval_board(self, board, max_turn):
        # filter out all completely empty lines i.e: [0, 0, 0, 0]
        state = [list(line) for line in self.get_streaks(board) if sum(line) != 0]

        streaks = []
        blocks = []
        # if not max_turn:
        # [1,0,0,0] || [1,1,0,0] || [1,1,1,0] || [1,1,1,1]
        streaks = [sum(line) for line in state if sum(line) <= 4]
        # [255,255,255,1]
        blocks = [1 for line in state if sum(line) == 766 and line.count(255) == 3]
        # else:
        #     # [255,0,0,0] || [255,255,0,0] || [255,255,255,0] || [255,255,255,255]
        #     streaks = [line.count(255) for line in state if sum(line) % 255 == 0]
        #     # [1,1,1,255]
        #     blocks = [1 for line in state if sum(line) == 258 and line.count(1) == 3]

        streak_score = self.attributes['in-a-row'] * len(streaks) + self.attributes['per-streak'] * sum(streaks)
        block_score = self.attributes['total-block'] * len(blocks)

        print("Streak Score:", streaks)
        print("Block Score:", block_score)
        print("-"*20)
        # time.sleep(1)
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