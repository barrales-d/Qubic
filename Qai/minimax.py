from random import randint
from math import inf
from GUI.constants import *
from GUI.buttons import *

from Qai.player import Player, returnStreaks

class MiniMaxPlayer(Player):
    def __init__(self, game, max_depth=10):
        super().__init__(game)
        self.move = None
        self.max_depth = max_depth

        self.image = pygame.image.load('./Graphics/ai_bot.png').convert_alpha()
        self.image = pygame.image.load('./Graphics/ship.gif').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.5)

    def draw(self, screen, render_area, board):
        pygame.draw.rect(screen, AI_BLUE, render_area)
        # TODO: draw a pixel ai_bot to use over the temp image 
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
        
        padding = 10
        screen.blit(self.image, (render_area[2] - self.image.get_width() - padding*2, render_area[1] + padding))

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
        streaks = returnStreaks(board)
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