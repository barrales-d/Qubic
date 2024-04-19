import random
import pygame
import os

from GUI.animator import Animator
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

        self.title_font = pygame.font.Font(None, 50)
        self.regular_font = pygame.font.Font(None, 25)

        bottom_panel_height = 125
        side_panel_width  = 150
        
        main_panel_width = WIDTH - side_panel_width
        main_panel_height = HEIGHT - bottom_panel_height
        padding = 10
        self.main_panel = (padding, padding, main_panel_width - padding, main_panel_height - padding)
        self.side_panel = (padding + WIDTH - side_panel_width, padding, side_panel_width - padding*2, main_panel_height - padding)
        self.bottom_panel = (padding, padding + HEIGHT - bottom_panel_height, WIDTH - padding*2, bottom_panel_height - padding)

        ai_position = (self.side_panel[0] + self.side_panel[2] // 2 + padding // 2, self.side_panel[3] - padding*6)
        self.animator = Animator('./Graphics/AIBot.png', 256, 3, 3, ai_position)
        self.animator.add('red', 100, 1, 4)
        self.animator.add('blue', 100, 5, 8)

    def play_game(self):
        while self.running:
            if self.game.getGameEnded(self.board, self.curr_player) != 0:
                self.running = False
                break

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
        # self.running = True
        # while self.running:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             self.running = False
        #             break
        #     self.draw()
        # return self.game.getGameEnded(self.board, self.curr_player)

        # pygame.quit()
    
    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, OFF_WHITE, self.main_panel, border_radius=PANEL_ROUNDED)
        padding = 10
        drawISOCubeGrid(self.screen, self.board, origin=[(self.main_panel[2] // 3) + padding, -100 + padding] , cellSize=23)

        self.draw_side()

        if(type(self.players[self.curr_player + 1]) == HumanPlayer):
            move = self.draw_human_board(self.board)
            self.players[self.curr_player + 1].set_move(move)
        else:
            self.draw_ai_board(self.board)

        self.clock.tick(FPS)
        # Update is called in the middle of game loop because AI.play runs until completion
        # So if it was a the bottom, the screen wouldn't update until after the AI algorithms complete
        # This way, the AI.draw() gets shown at least once before the game freezes
        pygame.display.update()
    
    def update(self):
        self.animator.update()
        canonical_board = self.game.getCanonicalForm(self.board, self.curr_player)
        action = self.players[self.curr_player + 1].play(canonical_board)
        if action == None: return

        if action == -1:
            self.running == False
            return
        valid_moves = [i for (i, valid) in enumerate(self.game.getValidMoves(canonical_board, self.curr_player)) if valid]
        if action in valid_moves:
            self.board, self.curr_player = self.game.getNextState(self.board, self.curr_player, action)
        else:
            rack = int(action / 16)
            row = int((action % 16) / 4)
            col = int((action % 16) % 4)
            print("ERROR: Trying to place piece at:", f'({rack}, {row}, {col})')
            self.players[self.curr_player].max_depth += 1
        #     print(self.curr_player)
        #     print(self.board)
        #     exit(1)

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
            self.animator.play('blue')
        else:
            self.animator.play('red')

        self.animator.draw(self.screen)
    
    def draw_side(self):
        # padding is 10 so (10 * 2)
        text_area = self.side_panel[2] - 20
        rect_size = 20

        pygame.draw.rect(self.screen, OFF_WHITE, self.side_panel, width=2, border_radius=PANEL_ROUNDED)
        
        text_pos = (self.side_panel[0] + self.side_panel[2] // 2, self.side_panel[1] + self.side_panel[3] // 3)
        display_text(self.screen, "Qubic", self.title_font, text_pos, width=text_area)

        text_pos = (text_pos[0], text_pos[1] + 45)
        display_text(self.screen, "Player 1: " + str(self.players[2]), self.regular_font, text_pos, width=text_area)

        rect_pos = (text_pos[0] - rect_size // 2 + self.side_panel[2] // 3, text_pos[1] - rect_size // 2)

        text_pos = (text_pos[0], text_pos[1] + 45)
        display_text(self.screen, "Player 2: " + str(self.players[0]), self.regular_font, text_pos, width=text_area)

        pygame.draw.rect(self.screen, RED, (rect_pos[0], rect_pos[1], rect_size, rect_size), border_radius=BTN_ROUNDED*2)
        
        rect_pos = (rect_pos[0], rect_pos[1] + 45)
        
        pygame.draw.rect(self.screen, BLUE, (rect_pos[0], rect_pos[1], rect_size, rect_size), border_radius=BTN_ROUNDED*2)



STATE_MENU = (1 << 0)
STATE_PLAY = (1 << 1)
STATE_END  = (1 << 3)

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Qubic")
    game = QubicGame(4, 4, 4)

    running = True
    state = STATE_MENU
    winner = None
    player1 = None
    player2 = None
    title_font = pygame.font.Font(None, 75)
    btn_font = pygame.font.Font(None, 35)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        if state == STATE_MENU:
            screen.fill(BLACK)
            center = [WIDTH // 2, HEIGHT // 3]
            display_text(screen, "QUBIC", title_font, center)
            center[1] += 100
            if textButton(screen, btn_font, "Human VS Human", center, BLACK, WHITE):
                player1 = HumanPlayer(game)
                player2 = HumanPlayer(game)
                state = STATE_PLAY
            
            center[1] += 50
            if textButton(screen, btn_font, "Human VS Mini Max", center, BLACK, WHITE):
                player1 = HumanPlayer(game)
                player2 = MiniMaxPlayer(game, 2, 2)
                state = STATE_PLAY

            center[1] += 50
            if textButton(screen, btn_font, "Human VS Alpha Beta", center, BLACK, WHITE):
                player1 = HumanPlayer(game)
                player2 = AlphaBetaPlayer(game, 2)
                state = STATE_PLAY

            center[1] += 50
            if textButton(screen, btn_font, "Mini Max VS Alpha Beta", center, BLACK, WHITE):
                player1 = MiniMaxPlayer(game, 1, 2)
                player2 = AlphaBetaPlayer(game, 2)
                state = STATE_PLAY

        elif state == STATE_PLAY:
            arena = Arena(screen, game, player1, player2)
            winner = arena.play_game()
            state = STATE_END

        elif state == STATE_END:
            winner_text = "It is a Draw!"
            if winner == 1:
                # print("Player 2 won!")
                winner_text = "Player 2 won!"
            elif winner == -1:
                # print("Player 1 won!")
                winner_text = "Player 1 won!"

            print(winner_text)
            # text_surface = title_font.render(winner_text, True, WHITE, BLACK)
            # text_rect = text_surface.get_rect(center = (WIDTH // 2, HEIGHT // 2))
            # screen.blit(text_surface, text_rect)
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()