import pygame

from GUI.constants import *
from GUI.buttons import *
from GUI.animator import Animator
from GUI.isometric import drawISOCubeGrid

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
        self.screen = screen
        self.running = True

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



STATE_MENU = (1 << 0)
STATE_PLAY = (1 << 1)
STATE_END  = (1 << 2)

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Qubic")
    game = QubicGame(4, 4, 4)
    py_clock = pygame.time.Clock()

    running = True
    state = STATE_MENU
    winner = None
    player1 = None
    player2 = None
    arena = None

    title_font = pygame.font.Font(None, 75)
    btn_font = pygame.font.Font(None, 35)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                state = STATE_END
                continue

        screen.fill(BLACK)
        if state == STATE_MENU:
            center = [WIDTH // 2, HEIGHT // 3]
            pygame.draw.rect(screen, OFF_WHITE, (center[0] - 200, center[1] - 100, 400, 400), width=BORDER_WIDTH, border_radius=PANEL_ROUNDED)

            display_text(screen, "QUBIC", title_font, center)
            center[1] += 100
            if textButton(screen, btn_font, "Human VS Human", center, BLACK, WHITE):
                player1 = HumanPlayer(game)
                player2 = HumanPlayer(game)
                arena = Arena(screen, game, player1, player2)
                state = STATE_PLAY
            
            center[1] += 50
            if textButton(screen, btn_font, "Human VS Mini Max", center, BLACK, WHITE):
                player1 = HumanPlayer(game)
                player2 = MiniMaxPlayer(game, 2, 2)
                arena = Arena(screen, game, player1, player2)
                state = STATE_PLAY

            center[1] += 50
            if textButton(screen, btn_font, "Human VS Alpha Beta", center, BLACK, WHITE):
                player1 = HumanPlayer(game)
                player2 = AlphaBetaPlayer(game, 2)
                arena = Arena(screen, game, player1, player2)
                state = STATE_PLAY

            center[1] += 50
            if textButton(screen, btn_font, "Mini Max VS Alpha Beta", center, BLACK, WHITE):
                player1 = MiniMaxPlayer(game, 1, 2)
                player2 = MiniMaxPlayer(game, 2, 2)
                # player2 = AlphaBetaPlayer(game, 2)
                arena = Arena(screen, game, player1, player2)
                state = STATE_PLAY

        elif state == STATE_PLAY:
            winner = game.getGameEnded(arena.board, arena.curr_player)
            if winner != 0:
                state = STATE_END
            arena.draw()
            arena.update()
            
        elif state == STATE_END:
            winner_text = "It is a Draw!"
            if winner == 1:     winner_text = "Player 2 won!"
            elif winner == -1:  winner_text = "Player 1 won!"

            arena.draw_board(arena.board)
            arena.draw_side()
            pygame.draw.rect(screen, OFF_WHITE, MAIN_PANEL, width=BORDER_WIDTH, border_radius=PANEL_ROUNDED)

            text_surface = title_font.render(winner_text, True, WHITE, BLACK)
            text_rect = text_surface.get_rect(center = (MAIN_PANEL[3] // 2, HEIGHT // 3))
            screen.blit(text_surface, text_rect)

            if textButton(screen, btn_font, "Restart", ((MAIN_PANEL[3] // 2 - 75, HEIGHT // 3 + 50)), BLACK, WHITE):
                state = STATE_MENU
                player1 = None
                player2 = None
                arena = None

            if textButton(screen, btn_font, "Quit", ((MAIN_PANEL[3] // 2 + 75, HEIGHT // 3 + 50)), BLACK, WHITE):
                running = False
                break

        py_clock.tick(FPS)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()