import random
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
        self.curr_player = 1
        self.board = self.game.getInitBoard()
        
        self.players = [player2, None, player1]
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.running = True

        bottom_panel_height = 125
        side_panel_width  = 150
        
        main_panel_width = WIDTH - side_panel_width
        main_panel_height = HEIGHT - bottom_panel_height
        padding = 10
        self.main_panel = (padding, padding, main_panel_width - padding, main_panel_height - padding)
        self.side_panel = (padding + WIDTH - side_panel_width, padding, side_panel_width - padding*2, main_panel_height - padding)
        self.bottom_panel = (padding, padding + HEIGHT - bottom_panel_height, WIDTH - padding*2, bottom_panel_height - padding)

        self.ai_avatar = pygame.image.load('./Graphics/ai_bot.png').convert_alpha()
        self.ai_avatar = pygame.transform.scale_by(self.ai_avatar, 0.5)

        self.ai_positions = [
            (self.bottom_panel[0] + self.ai_avatar.get_width() // 2 + padding*2, self.bottom_panel[1] + padding),
            (self.bottom_panel[2] - self.ai_avatar.get_width() - padding*2, self.bottom_panel[1] + padding),
            (self.main_panel[2] // 2 - self.main_panel[2] // 3 - self.ai_avatar.get_width() // 2, self.main_panel[3] - self.ai_avatar.get_height() + padding),
            (self.main_panel[2] // 2 + self.ai_avatar.get_width(), self.main_panel[3] - self.ai_avatar.get_height()  + padding)
        ]


    def play_game(self):        
        while self.running and self.game.getGameEnded(self.board, self.curr_player) == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("="*30)
                        print(self.players[self.curr_player + 1].returnStreaks(self.board))
            # draw
            self.draw()
            # update
            self.update()
        
        return self.game.getGameEnded(self.board, self.curr_player)

        # pygame.quit()
    
    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, OFF_WHITE, self.main_panel, border_radius=PANEL_ROUNDED)
        padding = 10
        drawISOCubeGrid(self.screen, self.board, origin=[(self.main_panel[2] // 3) + padding, -100 + padding] , cellSize=23)

        if(type(self.players[self.curr_player + 1]) == HumanPlayer):
            move = self.draw_human_board(self.board)
            self.players[self.curr_player + 1].set_move(move)
        else:
            self.draw_ai_board(self.board)

        self.draw_side()

        self.clock.tick(FPS)
        # Update is called in the middle of game loop because AI.play runs until completion
        # So if it was a the bottom, the screen wouldn't update until after the AI algorithms complete
        # This way, the AI.draw() gets shown at least once before the game freezes
        pygame.display.update()
    
    def update(self):
        action = self.players[self.curr_player + 1].play(self.game.getCanonicalForm(self.board, self.curr_player))
        if action != None:
            if action == -1:
                self.running == False
            else:
                self.board, self.curr_player = self.game.getNextState(self.board, self.curr_player, action)

    def draw_board(self, board):
        for rack in range(4):
            for row in range(4):
                for col in range(4):
                    pos_x = (BTN_SIZE + BTN_SPACING)*col + BTN_SPACING + (BTN_SIZE*6*rack) + self.bottom_panel[0]*6
                    pos_y = (BTN_SIZE + BTN_SPACING)*row + BTN_SPACING + 5

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
        pygame.draw.rect(self.screen, OFF_WHITE, self.bottom_panel, width=2, border_radius=PANEL_ROUNDED)
        return self.draw_board(board)
    
    def draw_ai_board(self, board):
        pygame.draw.rect(self.screen, OFF_WHITE, self.bottom_panel, width=2, border_radius=PANEL_ROUNDED)
        self.draw_board(board)

        if self.curr_player + 1 == 0:
            # blue ai
            pygame.draw.rect(self.screen, BLUE, (0, 0, 50, 50))
            pass
        else:
            # red ai
            pygame.draw.rect(self.screen, RED, (0, 0, 50, 50))
            pass

        self.screen.blit(self.ai_avatar, random.choice(self.ai_positions))
    
    def draw_side(self):
        title_font = pygame.font.Font(None, 50)
        regular_font = pygame.font.Font(None, 25)
        # padding is 10 so (10 * 2)
        text_area = self.side_panel[2] - 20
        rect_size = 20

        pygame.draw.rect(self.screen, OFF_WHITE, self.side_panel, width=2, border_radius=PANEL_ROUNDED)
        
        text_pos = (self.side_panel[0] + self.side_panel[2] // 2, self.side_panel[1] + self.side_panel[3] // 3)
        display_text(self.screen, "Qubic", title_font, text_pos, width=text_area)

        text_pos = (text_pos[0], text_pos[1] + 45)
        display_text(self.screen, "Player 1: " + str(self.players[2]), regular_font, text_pos, width=text_area)

        rect_pos = (text_pos[0] - rect_size // 2 + self.side_panel[2] // 3, text_pos[1] - rect_size // 2)

        text_pos = (text_pos[0], text_pos[1] + 45)
        display_text(self.screen, "Player 2: " + str(self.players[0]), regular_font, text_pos, width=text_area)

        pygame.draw.rect(self.screen, RED, (rect_pos[0], rect_pos[1], rect_size, rect_size), border_radius=BTN_ROUNDED*2)
        
        rect_pos = (rect_pos[0], rect_pos[1] + 45)
        
        pygame.draw.rect(self.screen, BLUE, (rect_pos[0], rect_pos[1], rect_size, rect_size), border_radius=BTN_ROUNDED*2)




def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Qubic")
    game = QubicGame(4, 4, 4)
    player1 = HumanPlayer(game)
    # player2 = HumanPlayer(game)
    # player1 = MiniMaxPlayer(game, 1, 2)
    player2 = MiniMaxPlayer(game, 2, 2)
    # player2 = AlphaBetaPlayer(game, 2)
    arena = Arena(screen, game, player1, player2)
    arena.play_game()


if __name__ == "__main__":
    main()