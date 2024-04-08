
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
        btn_size = 20
        spacing = 5
        self.move = None
        pygame.draw.rect(screen, LIGHT_BLUE, render_area)
        
        for rack in range(4):
            for row in range(4):
                for col in range(4):
                    pos_x = (btn_size + spacing)*col + spacing + (btn_size*6*rack)
                    pos_y = (btn_size + spacing)*row + spacing

                    cell = board[rack][row][col]
                    if cell != 0:
                        color = RED if cell == 1 else BLUE
                        createSquareButton(screen, pos_x, render_area[1] + pos_y, btn_size, btn_size, disabled=True, disabled_color=color)
                    else:
                        if createSquareButton(screen, pos_x, render_area[1] + pos_y, btn_size, btn_size):
                            self.move = 16 * rack + 4 * row + col
                    



    
    def play(self, board) -> int | None:
        if self.move != None:
            return self.move
        else:
            return None