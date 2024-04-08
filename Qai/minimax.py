from random import randint
from math import inf
from GUI.constants import *
from GUI.buttons import *

from Qai.player import Player

class MiniMaxPlayer(Player):
    def __init__(self, game, max_depth=10):
        super().__init__(game)
        self.move = -inf
        self.max_depth = max_depth

        self.font = pygame.font.Font(pygame.font.get_default_font(), 30)

    def draw(self, screen, render_area, board):
        pygame.draw.rect(screen, DARK_GREY, render_area)
        text_surface = self.font.render("AI is runnnig MiniMax...", True, WHITE)
        pos = (render_area[2] // 2, render_area[3] // 2 + render_area[1])
        text_rect = text_surface.get_rect(center = pos)
        screen.blit(text_surface, text_rect)
    
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
    
    def eval_board(self, board, max_turn):
        num1 = randint(-10, 10)
        num2 = randint(-10, 10)
        return max(num1, num2) if max_turn else min(num1, num2)

    
    def minimax(self, board, max_turn, depth=0):
        player = -1 if max_turn else 1
        if self.game.getGameEnded(board, player) != 0:
            return self.score(board, max_turn, depth)
        
        if depth >= self.max_depth:
            return self.eval_board(board, max_turn)
        
        # if (depth + 1) % 10 == 0:
        #     print("#######################\n", board)

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