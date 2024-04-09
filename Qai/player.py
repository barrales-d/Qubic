
from GUI.constants import *
from GUI.buttons import *

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