import pygame

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Qubic")

def displayGame(screen):
    bottom_panel_height = 125
    side_panel_width  = 150
    screen_width, screen_height = pygame.display.get_window_size()

    main_panel_width = screen_width - side_panel_width
    main_panel_height = screen_height - bottom_panel_height

    displayMainPanel(screen, main_panel_width, main_panel_height)
    displaySidePanel(screen, side_panel_width, main_panel_height)
    displayBottomPanel(screen, bottom_panel_height)


def displayMainPanel(screen, width, height):
    pygame.draw.rect(screen, pygame.Color(0, 255, 0), (0, 0, width, height))

def displaySidePanel(screen, width, height):
    screen_width, _ = pygame.display.get_window_size()
    pygame.draw.rect(screen, pygame.Color(255, 0, 0), (screen_width - width, 0, screen_width, height))

def displayBottomPanel(screen, size):
    width, height = pygame.display.get_window_size()
    pygame.draw.rect(screen, pygame.Color(0, 0, 255), (0, height - size, width, height))

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displayGame(screen)

    fpsClock.tick(fps)
    pygame.display.update()

pygame.quit()

