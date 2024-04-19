import pygame

from GUI.constants import *
BTN_COL = OFF_WHITE
BTN_H_COL = DARK_GREY

MOUSE_BTN_1 = 0
BTN_ROUNDED = 2
BTN_SIZE = 24
BTN_SPACING = 2

def createSquareButton(screen, x, y, w, h, disabled=False, disabled_color=GREY):
    btn_rect = pygame.rect.Rect((x, y, w, h))
    mouse_pos = pygame.mouse.get_pos()
    hovered = btn_rect.collidepoint(mouse_pos)
    btn_color = BTN_COL
    btn_outline = BTN_H_COL
    if(hovered):
        btn_color = BTN_H_COL
        btn_outline = BTN_COL

    
    btn_color = btn_color if not disabled else disabled_color
    pygame.draw.rect(screen, btn_color, btn_rect, border_radius=BTN_ROUNDED)
    pygame.draw.rect(screen, btn_outline, btn_rect, BTN_SPACING, border_radius=BTN_ROUNDED)
    
    if not disabled:
        if(pygame.mouse.get_pressed()[MOUSE_BTN_1]):
            if(hovered):
                return True
    
    return False

def textButton(screen, font, text, pos, btn_color=BTN_COL, btn_outline=BTN_H_COL):
    text_surface = font.render(text, True, btn_outline)
    text_rect = text_surface.get_rect(center = pos)

    btn_rect = text_rect.inflate(30, 15)

    mouse_pos = pygame.mouse.get_pos()
    hovered = btn_rect.collidepoint(mouse_pos)
    
    if(hovered):
        btn_color, btn_outline = btn_outline, btn_color
        text_surface = font.render(text, True, btn_outline)
    
    pygame.draw.rect(screen, btn_color, btn_rect, border_radius=BTN_ROUNDED)
    pygame.draw.rect(screen, btn_outline, btn_rect, BTN_SPACING, border_radius=BTN_ROUNDED)
    screen.blit(text_surface, text_rect)
    
    if(pygame.mouse.get_pressed()[MOUSE_BTN_1]):
        if(hovered):
            return True
    
    return False