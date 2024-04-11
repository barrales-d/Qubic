
import numpy as np
from GUI.constants import *
from GUI.buttons import *

# Copied from GameLogic.board
def returnStreaks(board):
    streak = np.zeros((76, 4), dtype=np.uint8)

    # ULTRA DIAGONALS in 3D

    # From front, top left
    streak[0] = [board[0, 0, 0],
                    board[1, 1, 1],
                    board[2, 2, 2],
                    board[3, 3, 3]]

    # From back, top left
    streak[1] = [board[3, 0, 0],
                    board[2, 1, 1],
                    board[1, 2, 2],
                    board[0, 3, 3]]

    # From front, bottom left
    streak[2] = [board[0, 3, 0],
                    board[1, 2, 1],
                    board[2, 1, 2],
                    board[3, 0, 3]]

    # From back, bottom left
    streak[3] = [board[3, 3, 0],
                    board[2, 2, 1],
                    board[1, 1, 2],
                    board[0, 0, 3]]

    # CHECK ANTI/DIAGONALS in 2D
    for cut in range(4):
        # DIAGONALS by LAYER
        streak[cut + 4] = [board[cut, 0, 0],
                            board[cut, 1, 1],
                            board[cut, 2, 2],
                            board[cut, 3, 3]]

        # ANTI DIAGONALS by LAYER
        streak[cut + 8] = [board[cut, 0, 3],
                            board[cut, 1, 2],
                            board[cut, 2, 1],
                            board[cut, 3, 0]]

        # DIAGONALS by ROW
        streak[cut + 12] = [board[0, cut, 0],
                            board[1, cut, 1],
                            board[2, cut, 2],
                            board[3, cut, 3]]

        # ANTI DIAGONALS by ROW
        streak[cut + 16] = [board[0, cut, 3],
                            board[1, cut, 2],
                            board[2, cut, 1],
                            board[3, cut, 0]]

        # DIAGONALS by COL
        streak[cut + 20] = [board[0, 0, cut],
                            board[1, 1, cut],
                            board[2, 2, cut],
                            board[3, 3, cut]]

        # ANTI DIAGONALS by COL
        streak[cut + 24] = [board[0, 3, cut],
                            board[1, 2, cut],
                            board[2, 1, cut],
                            board[3, 0, cut]]

    index = 28
    # STACK POINTS
    for row in range(4):
        for col in range(4):
            streak[index] = board[0:4, row, col]
            index = index + 1
    # ROW POINTS
    for stack in range(4):
        for row in range(4):
            streak[index] = board[stack, row, 0:4]
            index = index + 1
    # COL POINTS
    for stack in range(4):
        for col in range(4):
            streak[index] = board[stack, 0:4, col]
            index = index + 1

    return streak

class Player:
    def __init__(self, game):
        self.game = game
    
    def draw(self, screen, render_area, board):
        pass

    def play(self, board) -> int | None:
        pass


class HumanPlayer(Player):
    def __init__(self, game):
        super().__init__(game)

        self.move = None

    def draw(self, screen, render_area, board):
        self.move = None
        pygame.draw.rect(screen, LIGHT_BLUE, render_area)
        
        for rack in range(4):
            for row in range(4):
                for col in range(4):
                    pos_x = (BTN_SIZE + BTN_SPACING)*col + BTN_SPACING + (BTN_SIZE*6*rack)
                    pos_y = (BTN_SIZE + BTN_SPACING)*row + BTN_SPACING

                    cell = board[rack][row][col]
                    if cell != 0:
                        color = RED if cell == 1 else BLUE
                        createSquareButton(screen, pos_x, render_area[1] + pos_y, BTN_SIZE, BTN_SIZE, disabled=True, disabled_color=color)
                    else:
                        if createSquareButton(screen, pos_x, render_area[1] + pos_y, BTN_SIZE, BTN_SIZE):
                            self.move = 16 * rack + 4 * row + col
                    



    
    def play(self, board) -> int | None:
        if self.move != None:
            return self.move
        else:
            return None