from random import randint

class MinMaxPlayer:
    def __init__(self, game):
        self.game = game

    def has_filled_board(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
        for x in valid_moves:
            # there is still moves to be played 
            if x:
                return x
            
        return False
    
    def has_won(self, board, player):
        # TODO: check all possible winning combinations
        return randint(0, 1)

    def minmax(self, board):
        # determine if board if terminal state
        if self.has_won(board, 1):
            return 1
        elif self.has_won(board, -1):
            return -1
        elif self.has_filled_board(board):
            return 0
        
        empty_cells = [i for (i, valid) in enumerate(self.game.getValidMoves(board, 1)) if valid]
        # otherwise determine if the current play is for minimizing or maximizing
        #   in other word, is the current move the AI's or human move
        
        move = 1 # TODO: determine the correct move to filled the board with  

        best_move_idx = None
        for cell_idx in empty_cells:
            current_state = board
            board[cell_idx] = move
            
            current_move_idx = None
            if move == 1:
                # TODO: create max_value function
                current_move_idx = self.max_value(board)
            else:
                # TODO: create min_value function and maybe name them better
                current_move_idx = self.min_value(board)

            if best_move_idx is None or best_move_idx < current_move_idx:
                best_move_idx = current_move_idx

            # change the board back to the current_state each iteration
            board = current_state

        # return value from either function: 
        # if AI's, run max_value(board)
        # if human's, run min_value(board)
        return best_move_idx

    def play(self, board):
        # TODO: create minmax algorithm for Qubic game
        # TODO: create copy of board to pass to minmax function
        # get all empty cells in a list
        # go through each cell and run minmax on each cell
        # collect the best moves from each minimax and return that move?
        
        
        # Generate the whole game tree to leaves

        # Apply utility (payoff) function to leaves.

        # Use DFS for expanding the tree.

        # Back-up values from the leaves towards the root. A MAX node computes the maximum value from its child values. A MIN node
        # computes the minimum value from its child values.

        # When value reaches the root: optimal move is determined.
        valid_moves = self.game.getValidMoves(board, 1)
        print("\nMoves:", [i for (i, valid) in enumerate(valid_moves) if valid])

        while True:
            move = int(input())
            if valid_moves[move]:
                break
            else:
                print("Invalid move")
        return move
