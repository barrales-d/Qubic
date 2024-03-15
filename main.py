from GameLogic.qubic import QubicGame, display
from GameLogic.player import HumanQubicPlayer
from GameLogic.arena import Arena

from Qai.minmax import MinMaxPlayer

game = QubicGame(4, 4, 4)

# player1 = HumanQubicPlayer(game).play
player1 = MinMaxPlayer(game).play
player2 = HumanQubicPlayer(game).play

player_list = [player1, player2]

arena = Arena(player1, player2, game, display=display)
print(arena.playGame(verbose=True))
