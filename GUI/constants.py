BLACK = (0, 0, 0)
GREY = (160, 160, 160)
DARK_GREY = (80, 80, 80)
WHITE = (255, 255, 255)
RED = (160, 0, 0)
BLUE = (0, 0, 160)
LIGHT_BLUE = (200, 200, 255)

AI_BLUE = (56, 81, 119)


FPS = 30
WIDTH = 640
HEIGHT = 480

def display_text(screen, font, pos, text):
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center = pos)
        screen.blit(text_surface, text_rect)