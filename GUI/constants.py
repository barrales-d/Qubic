BLACK = (0, 0, 0)
GREY = (160, 160, 160)
DARK_GREY = (80, 80, 80)
WHITE = (255, 255, 255)
OFF_WHITE = (240, 249, 255)
RED = (160, 0, 0)
BLUE = (0, 0, 160)
LIGHT_BLUE = (200, 200, 255)

AI_BLUE = (56, 81, 119)


FPS = 60
WIDTH = 640
HEIGHT = 640
# global padding
GPAD = 10

BP_HEIGHT = 125
SP_WIDTH  = 150
# MAIN PANEL
MP_WIDTH = WIDTH - SP_WIDTH
MP_HEIGHT = HEIGHT - BP_HEIGHT

MAIN_PANEL = (GPAD, GPAD, MP_WIDTH - GPAD, MP_HEIGHT - GPAD)
SIDE_PANEL = (GPAD + WIDTH - SP_WIDTH, GPAD, SP_WIDTH - GPAD*2, MP_HEIGHT - GPAD)
BOTTOM_PANEL = (GPAD, GPAD + HEIGHT - BP_HEIGHT, WIDTH - GPAD*2, BP_HEIGHT - GPAD)


PANEL_ROUNDED = 25

def display_text(screen, text, font, pos, width=0):
    text_surface = font.render(text, True, WHITE, wraplength=width)
    text_rect = text_surface.get_rect(center = pos)
    screen.blit(text_surface, text_rect)