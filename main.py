import pygame
from GUI.constants import *
from GUI.isometric import drawISOCubeGrid

# from Qai.human_player import HumanPlayer
from Qai.player import HumanPlayer
from Qai.minimax import MiniMaxPlayer

from GameLogic.qubic import QubicGame


class Arena():
    def __init__(self, game, player1, player2):
        self.game = game
        self.players = [player2, None, player1]
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        pygame.display.set_caption("Qubic")


        bottom_panel_height = 125
        side_panel_width  = 150
        
        main_panel_width = WIDTH - side_panel_width
        main_panel_height = HEIGHT - bottom_panel_height
        
        self.main_panel = (0, 0, main_panel_width, main_panel_height)
        self.side_panel = (WIDTH - side_panel_width, 0, WIDTH, main_panel_height)
        self.bottom_panel = (0, HEIGHT - bottom_panel_height, WIDTH, bottom_panel_height)


    def playGame(self):
        curr_player = 1
        board = self.game.getInitBoard()
        
        while self.running and self.game.getGameEnded(board, curr_player) == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
            # update
            action = self.players[curr_player + 1].play(self.game.getCanonicalForm(board, curr_player))
            if action == -1:
                self.running == False
                break
            if(action):
                board, curr_player = self.game.getNextState(board, curr_player, action)

            # draw
            pygame.draw.rect(self.screen, GREY, self.main_panel)
            drawISOCubeGrid(self.screen, board, origin=[(self.main_panel[2] // 3), -100], cellSize=16)

            self.players[curr_player + 1].draw(self.screen, self.bottom_panel, board)


            self.clock.tick(FPS)
            pygame.display.update()
        pygame.quit()




def main():
    pygame.init()

    pygame.font.init()

    game = QubicGame(4, 4, 4)
    player1 = HumanPlayer(game)
    player2 = MiniMaxPlayer(game, 2)


    arena = Arena(game, player1, player2)
    arena.playGame()


if __name__ == "__main__":
    main()