import pygame

from GUI.constants import *

from Qai.player import HumanPlayer
from Qai.minimax import MiniMaxPlayer
from Qai.alphabeta import AlphaBetaPlayer

from GUI.buttons import *
from GUI.arena import Arena

from GameLogic.qubic import QubicGame

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
                player2 = MiniMaxPlayer(game, False, 2)
                arena = Arena(screen, game, player1, player2)
                state = STATE_PLAY

            center[1] += 50
            if textButton(screen, btn_font, "Human VS Alpha Beta", center, BLACK, WHITE):
                player1 = HumanPlayer(game)
                player2 = AlphaBetaPlayer(game, False, 2)
                arena = Arena(screen, game, player1, player2)
                state = STATE_PLAY

            center[1] += 50
            if textButton(screen, btn_font, "Mini Max VS Alpha Beta", center, BLACK, WHITE):
                player1 = MiniMaxPlayer(game, True, 2)
                player2 = AlphaBetaPlayer(game, True, 2)
                arena = Arena(screen, game, player1, player2)
                state = STATE_PLAY
        elif state == STATE_PLAY:

            # winner, _ = arena.get_winning_streak()
            if arena.get_winning_streak()[0] != 0:
                state = STATE_END
                continue
            # winner = game.getGameEnded(game.getCanonicalForm(arena.board, 1), 1)
            # if winner != 0:
            #     state = STATE_END
            #     continue

            # winner = game.getGameEnded(game.getCanonicalForm(arena.board, -1), -1)
            # if winner != 0:
            #     state = STATE_END
            #     continue

            arena.draw()
            arena.update()
        elif state == STATE_END:
            winner, winning_streak = arena.get_winning_streak()
            winner_text = "It is a Draw!"
            if winner == 1:     winner_text = "Player 1 won!"
            elif winner == -1:  winner_text = "Player 2 won!"

            arena.draw_board(arena.board)

            if winning_streak != None:
                for cell in winning_streak:
                    rack, row, col = cell
                    pos_x = (BTN_SIZE + BTN_SPACING)*col + BTN_SPACING + (BTN_SIZE*6*rack) + BOTTOM_PANEL[0]*6
                    pos_y = (BTN_SIZE + BTN_SPACING)*row + BTN_SPACING + 5
                    smallButton(screen, pos_x, BOTTOM_PANEL[1] + pos_y, disabled=True, disabled_color=GREEN)


            arena.draw_side()
            pygame.draw.rect(screen, OFF_WHITE, MAIN_PANEL, width=BORDER_WIDTH, border_radius=PANEL_ROUNDED)

            # print(arena.get_winning_streak())
            # exit(0)

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