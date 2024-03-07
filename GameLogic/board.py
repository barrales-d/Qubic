from collections import namedtuple
import numpy as np

DEFAULT_HEIGHT = 4
DEFAULT_WIDTH = 4
DEFAULT_DEPTH = 4
DEFAULT_WIN_LENGTH = 4

WinState = namedtuple('WinState', 'is_ended winner')


class Board():
    """
    Qubic Board.
    """

    def __init__(self, height=None, width=None, depth = None, win_length=None, np_pieces=None):
        "Set up initial board configuration."
        self.height = height or DEFAULT_HEIGHT
        self.width = width or DEFAULT_WIDTH
        self.depth = depth or DEFAULT_DEPTH
        self.win_length = win_length or DEFAULT_WIN_LENGTH

        if np_pieces is None:
            self.np_pieces = np.zeros([self.depth, self.height, self.width])
        else:
            self.np_pieces = np_pieces
            assert self.np_pieces.shape == (self.depth, self.height, self.width)

    def add_piece(self, action, player):
        "Set given location of board to the player type."
        rack = int(action / 16)
        row = int((action % 16) / 4)
        col = int((action % 16) % 4)
        if(self.np_pieces[rack][row][col] != 0):
            raise ValueError("Can't play position [%s,%s,%s] on board %s" % (rack,row,col, self))

        self.np_pieces[rack][row][col] = player

    def get_valid_moves(self):
        "Any zero value in the cube is a valid move"
        valids = np.zeros(self.depth*self.height*self.width, dtype=bool)
        for i in range(self.depth):
            for j in range(self.height):
                for k in range(self.width):
                    if(self.np_pieces[i][j][k] == 0):
                        valids[16*i+4*j+k] = 1
        return valids


    def get_win_state(self):
        streaks = self.returnStreaks(self.np_pieces)
        for streak in streaks:
            if(np.unique(streak).size == 1):
                for player in [-1, 1]:
                    if streak[0] == player:
                        return WinState(True, player)

        # draw has very little value.
        if not self.get_valid_moves().any():
            return WinState(True, None)

        # Game is not ended yet.
        return WinState(False, None)

    def with_np_pieces(self, np_pieces):
        """Create copy of board with specified pieces."""
        if np_pieces is None:
            np_pieces = self.np_pieces
        return Board(self.height, self.width, self.depth, self.win_length, np_pieces)


    def returnStreaks(self, board):
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


    def __str__(self):
        return str(self.np_pieces)