import numpy as np
import pygame

from GUI.constants import *
from GUI.buttons import *
from GUI.animator import Animator
from GUI.isometric import drawISOCubeGrid

from Qai.player import HumanPlayer

from Qai.streaks import return_streak_indicies, returnStreaks

class Arena():
    def __init__(self, screen, game, player1, player2):
        self.game = game
        self.curr_player = 1
        self.board = self.game.getInitBoard()

        self.players = [player2, None, player1]
        self.screen = screen

        self.title_font = pygame.font.Font(None, 50)
        self.regular_font = pygame.font.Font(None, 25)

        ai_position = (SIDE_PANEL[0] + SIDE_PANEL[2] // 2 + GPAD // 2, SIDE_PANEL[3] - GPAD*6)
        self.animator = Animator('./Graphics/AIBot.png', 256, 3, 3, ai_position)
        self.animator.add('red', 100, 1, 4)
        self.animator.add('blue', 100, 5, 8)

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, OFF_WHITE, MAIN_PANEL, border_radius=PANEL_ROUNDED)
        drawISOCubeGrid(self.screen, self.board, origin=[(MAIN_PANEL[2] // 3) + GPAD, -100 + GPAD] , cellSize=23)

        self.draw_side()

        if(type(self.players[self.curr_player + 1]) == HumanPlayer):
            move = self.draw_board(self.board)
            self.players[self.curr_player + 1].set_move(move)
        else:
            self.draw_ai_board(self.board)

        # Update is called in the middle of game loop because AI.play runs until completion
        # So if it was a the bottom, the screen wouldn't update until after the AI algorithms complete
        # This way, the AI.draw() gets shown at least once before the game freezes
        pygame.display.update()

    def update(self):
        self.animator.update()
        canonical_board = self.game.getCanonicalForm(self.board, self.curr_player)
        action = self.players[self.curr_player + 1].play(canonical_board)
        if action == None: return

        valid_moves = [i for (i, valid) in enumerate(self.game.getValidMoves(canonical_board, 1)) if valid]
        if action in valid_moves:
            self.board, self.curr_player = self.game.getNextState(self.board, self.curr_player, action)
        else:
            rack = int(action / 16)
            row = int((action % 16) / 4)
            col = int((action % 16) % 4)
            print("ERROR: Trying to place piece at:", f'({rack}, {row}, {col})')
            self.players[self.curr_player].max_depth += 1

    def get_winning_streak(self):
        streaks = returnStreaks(self.board)
        streak_indicies = return_streak_indicies(self.board)
        for idx, streak in enumerate(streaks):
            if(np.unique(streak).size == 1):
                for player in [255, 1]:
                    if streak[0] == player:
                        if player == 255: player = -1

                        return player, list(streak_indicies[idx])
        # draw
        if not self.game.getValidMoves(self.board, self.curr_player).any():
            return None, None

        # Game is not ended yet.
        return 0, None


    def draw_board(self, board):
        pygame.draw.rect(self.screen, OFF_WHITE, BOTTOM_PANEL, width=BORDER_WIDTH, border_radius=PANEL_ROUNDED)
        for rack in range(4):
            for row in range(4):
                for col in range(4):
                    pos_x = (BTN_SIZE + BTN_SPACING)*col + BTN_SPACING + (BTN_SIZE*6*rack) + BOTTOM_PANEL[0]*6
                    pos_y = (BTN_SIZE + BTN_SPACING)*row + BTN_SPACING + 5

                    cell = board[rack][row][col]
                    color = GREY
                    if cell == 1: color = RED
                    if cell == -1: color = BLUE

                    if cell == 0:
                        if smallButton(self.screen, pos_x, BOTTOM_PANEL[1] + pos_y):
                            return 16 * rack + 4 * row + col
                    else:
                        smallButton(self.screen, pos_x, BOTTOM_PANEL[1] + pos_y, disabled=True, disabled_color=color)

    def draw_ai_board(self, board):
        self.draw_board(board)

        if self.curr_player + 1 == 0:
            self.animator.play('blue')
        else:
            self.animator.play('red')

        self.animator.draw(self.screen)

    def draw_side(self):
        text_area = SIDE_PANEL[2] - GPAD * 2
        rect_size = GPAD * 2

        pygame.draw.rect(self.screen, OFF_WHITE, SIDE_PANEL, width=BORDER_WIDTH, border_radius=PANEL_ROUNDED)

        text_pos = (SIDE_PANEL[0] + SIDE_PANEL[2] // 2, SIDE_PANEL[1] + SIDE_PANEL[3] // 3)
        display_text(self.screen, "Qubic", self.title_font, text_pos, width=text_area)

        text_pos = (text_pos[0], text_pos[1] + 45)
        display_text(self.screen, "Player 1: " + str(self.players[2]), self.regular_font, text_pos, width=text_area)

        rect_pos = (text_pos[0] - rect_size // 2 + SIDE_PANEL[2] // 3, text_pos[1] - rect_size // 2)

        text_pos = (text_pos[0], text_pos[1] + 45)
        display_text(self.screen, "Player 2: " + str(self.players[0]), self.regular_font, text_pos, width=text_area)

        pygame.draw.rect(self.screen, RED, (rect_pos[0], rect_pos[1], rect_size, rect_size), border_radius=BTN_ROUNDED*2)

        rect_pos = (rect_pos[0], rect_pos[1] + 45)

        pygame.draw.rect(self.screen, BLUE, (rect_pos[0], rect_pos[1], rect_size, rect_size), border_radius=BTN_ROUNDED*2)