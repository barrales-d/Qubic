import numpy as np


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

def return_streak_indicies(board):
    streak = np.zeros((76, 4), dtype=object)


    # ULTRA DIAGONALS in 3D

    # From front, top left
    streak[0] = [(0, 0, 0),
                    (1, 1, 1),
                    (2, 2, 2),
                    (3, 3, 3)]

    # From back, top left
    streak[1] = [(3, 0, 0),
                    (2, 1, 1),
                    (1, 2, 2),
                    (0, 3, 3)]

    # From front, bottom left
    streak[2] = [(0, 3, 0),
                    (1, 2, 1),
                    (2, 1, 2),
                    (3, 0, 3)]

    # From back, bottom left
    streak[3] = [(3, 3, 0),
                    (2, 2, 1),
                    (1, 1, 2),
                    (0, 0, 3)]

    # CHECK ANTI/DIAGONALS in 2D
    for cut in range(4):
        # DIAGONALS by LAYER
        streak[cut + 4] = [(cut, 0, 0),
                            (cut, 1, 1),
                            (cut, 2, 2),
                            (cut, 3, 3)]

        # ANTI DIAGONALS by LAYER
        streak[cut + 8] = [(cut, 0, 3),
                            (cut, 1, 2),
                            (cut, 2, 1),
                            (cut, 3, 0)]

        # DIAGONALS by ROW
        streak[cut + 12] = [(0, cut, 0),
                            (1, cut, 1),
                            (2, cut, 2),
                            (3, cut, 3)]

        # ANTI DIAGONALS by ROW
        streak[cut + 16] = [(0, cut, 3),
                            (1, cut, 2),
                            (2, cut, 1),
                            (3, cut, 0)]

        # DIAGONALS by COL
        streak[cut + 20] = [(0, 0, cut),
                            (1, 1, cut),
                            (2, 2, cut),
                            (3, 3, cut)]

        # ANTI DIAGONALS by COL
        streak[cut + 24] = [(0, 3, cut),
                            (1, 2, cut),
                            (2, 1, cut),
                            (3, 0, cut)]

    index = 28
    # STACK POINTS
    for row in range(4):
        for col in range(4):
            streak[index] = [(0, row, col),
                             (1, row, col),
                             (2, row, col),
                             (3, row, col)]
            index = index + 1
    # ROW POINTS
    for stack in range(4):
        for row in range(4):
            streak[index] = [(stack, row, 0),
                             (stack, row, 1),
                             (stack, row, 2),
                             (stack, row, 3)]
            index = index + 1
    # COL POINTS
    for stack in range(4):
        for col in range(4):
            streak[index] = [(stack, 0, col),
                             (stack, 1, col),
                             (stack, 2, col),
                             (stack, 3, col)]
            index = index + 1

    return streak