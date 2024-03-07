# import pygame

# pygame.init()

# fps = 60
# fpsClock = pygame.time.Clock()

# width, height = 640, 480
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Qubic")

# # Game loop.
# running = True
# while running:
#   screen.fill((0, 0, 0))

#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       running = False

#   fpsClock.tick(fps)

#   pygame.display.update()

# pygame.quit()

from GameLogic.qubic import QubicGame

game = QubicGame(4, 4, 4)