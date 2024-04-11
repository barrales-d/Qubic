from random import randint
from math import inf
from GUI.constants import *
from GUI.buttons import *

from Qai.player import Player

class AlphaBetaPlayer(Player):
    def __init__(self, game, max_depth=10):
        super().__init__(game)
        self.move = -inf
        self.max_depth = max_depth
        self.font = pygame.font.Font(pygame.font.get_default_font(), 28)

    def draw(self, screen, render_area, board):
        pygame.draw.rect(screen, AI_BLUE, render_area)
        
        for rack in range(4):
            for row in range(4):
                for col in range(4):
                    pos_x = (BTN_SIZE + BTN_SPACING)*col + BTN_SPACING + (BTN_SIZE*6*rack)
                    pos_y = (BTN_SIZE + BTN_SPACING)*row + BTN_SPACING

                    cell = board[rack][row][col]
                    color = GREY
                    if cell == 1: color = RED
                    if cell == -1: color = BLUE
                    
                    createSquareButton(screen, pos_x, render_area[1] + pos_y, BTN_SIZE, BTN_SIZE, disabled=True, disabled_color=color)
    
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
        num1 = randint(-10, 10)
        num2 = randint(-10, 10)
        return max(num1, num2) if max_turn else min(num1, num2)

    
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