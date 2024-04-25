import numpy as np
from GUI.constants import *
from GUI.buttons import *

class Player:
    def __init__(self, game):
        self.game = game

    def play(self, board) -> int | None:
        pass

    # AI attributes scalars
    attributes = {
        'in-a-row': 0.25,
        'per-streak': 0.55,
        'total-block': 0.925,
    }


class HumanPlayer(Player):
    def __init__(self, game):
        super().__init__(game)
        self.move = None
    
    def __str__(self) -> str: return "Human"

    def set_move(self, move):
        self.move = move
    
    def play(self, board) -> int | None:
        return self.move