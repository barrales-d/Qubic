import pygame
import os

from GUI.buttons import *
from GUI.constants import *
from GUI.isometric import drawISOCubeGrid

# from Qai.human_player import HumanPlayer
from Qai.player import HumanPlayer
from Qai.minimax import MiniMaxPlayer
from Qai.alphabeta import AlphaBetaPlayer

from GameLogic.qubic import QubicGame


class Arena():
    def __init__(self, screen, game, player1, player2):
        self.game = game
        self.players = [player2, None, player1]
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.running = True

        bottom_panel_height = 125
        side_panel_width  = 150
        
        main_panel_width = WIDTH - side_panel_width
        main_panel_height = HEIGHT - bottom_panel_height
        
        self.main_panel = (0, 0, main_panel_width, main_panel_height)
        self.side_panel = (WIDTH - side_panel_width, 0, WIDTH, main_panel_height)
        self.bottom_panel = (0, HEIGHT - bottom_panel_height, WIDTH, bottom_panel_height)

        self.ai_avatar = pygame.image.load('./Graphics/ai_bot.png').convert_alpha()
        self.ai_avatar = pygame.transform.scale_by(self.ai_avatar, 0.5)


    def play_game(self):
        curr_player = 1
        board = self.game.getInitBoard()
        
        while self.running and self.game.getGameEnded(board, curr_player) == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
            # update
            action = self.players[curr_player + 1].play(self.game.getCanonicalForm(board, curr_player))
            if action != None:
                if action == -1:
                    self.running == False
                    break
                else:
                    board, curr_player = self.game.getNextState(board, curr_player, action)
            # draw
            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, GREY, self.main_panel)
            drawISOCubeGrid(self.screen, board, origin=[(self.main_panel[2] // 3), -100], cellSize=16)

            if(type(self.players[curr_player + 1]) == HumanPlayer):
                move = self.draw_human_board(board)
                self.players[curr_player + 1].set_move(move)
            else:
                self.draw_ai_board(board)



            print("continuing rendering screen")
            self.clock.tick(FPS)
            # Update is called in the middle of game loop because AI.play runs until completion
            # So if it was a the bottom, the screen wouldn't update until after the AI algorithms complete
            # This way, the AI.draw() gets shown at least once before the game freezes
            pygame.display.update()
        
        return self.game.getGameEnded(board, curr_player)

        # pygame.quit()

    def draw_board(self, board):
        for rack in range(4):
            for row in range(4):
                for col in range(4):
                    pos_x = (BTN_SIZE + BTN_SPACING)*col + BTN_SPACING + (BTN_SIZE*6*rack)
                    pos_y = (BTN_SIZE + BTN_SPACING)*row + BTN_SPACING

                    cell = board[rack][row][col]
                    color = GREY
                    if cell == 1: color = RED
                    if cell == -1: color = BLUE

                    if cell == 0:
                        if createSquareButton(self.screen, pos_x, self.bottom_panel[1] + pos_y, BTN_SIZE, BTN_SIZE):
                            return 16 * rack + 4 * row + col
                    else:
                        createSquareButton(self.screen, pos_x, self.bottom_panel[1] + pos_y, BTN_SIZE, BTN_SIZE, disabled=True, disabled_color=color)
    
    def draw_human_board(self, board):
        pygame.draw.rect(self.screen, LIGHT_BLUE, self.bottom_panel)
        return self.draw_board(board)
    
    def draw_ai_board(self, board):
        pygame.draw.rect(self.screen, AI_BLUE, self.bottom_panel)
        self.draw_board(board)

        padding = 10
        self.screen.blit(self.ai_avatar, (self.bottom_panel[2] - self.ai_avatar.get_width() - padding*2, self.bottom_panel[1] + padding))




def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Qubic")
    game = QubicGame(4, 4, 4)

    player1 = HumanPlayer(game)
    # player2 = HumanPlayer(game)
    # player1 = AlphaBetaPlayer(game, 2)
    player2 = MiniMaxPlayer(game, 2)
    arena = Arena(screen, game, player1, player2)
    arena.play_game()


if __name__ == "__main__":
    main()