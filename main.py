import pygame
import os

from GUI.constants import *
from GUI.isometric import drawISOCubeGrid

# from Qai.human_player import HumanPlayer
from Qai.player import HumanPlayer, returnStreaks
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


    def playGame(self):
        curr_player = 1
        board = self.game.getInitBoard()
        
        while self.running and self.game.getGameEnded(board, curr_player) == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        streaks = returnStreaks(board)
                        # print(streaks)
                        os.system('clear')
                        for streak in streaks:
                            print(streak, sum(streak))
                            print("=======================")
                        
            # draw
            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, GREY, self.main_panel)
            drawISOCubeGrid(self.screen, board, origin=[(self.main_panel[2] // 3), -100], cellSize=16)

            self.players[curr_player + 1].draw(self.screen, self.bottom_panel, board)
            self.clock.tick(FPS)
            # Update is called in the middle of game loop because AI.play runs until completion
            # So if it was a the bottom, the screen wouldn't update until after the AI algorithms complete
            # This way, the AI.draw() gets shown at least once before the game freezes
            pygame.display.update()

            # update
            action = self.players[curr_player + 1].play(self.game.getCanonicalForm(board, curr_player))
            if action != None:
                if action == -1:
                    self.running == False
                    break
                else:
                    board, curr_player = self.game.getNextState(board, curr_player, action)

        pygame.quit()




def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Qubic")

    game = QubicGame(4, 4, 4)
    # player1 = HumanPlayer(game)
    # player2 = HumanPlayer(game)
    player1 = AlphaBetaPlayer(game, 2)
    player2 = MiniMaxPlayer(game, 2)

    arena = Arena(screen, game, player1, player2)
    arena.playGame()


if __name__ == "__main__":
    main()