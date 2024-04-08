import pygame

from GUI.constants import *
BTN_COL = GREY
BTN_H_COL = DARK_GREY

MOUSE_BTN_1 = 0
BTN_ROUNDED = 5

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
    pygame.draw.rect(screen, btn_color, btn_rect, 0, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED)
    pygame.draw.rect(screen, btn_outline, btn_rect, 2, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED, BTN_ROUNDED)
    
    if not disabled:
        if(pygame.mouse.get_pressed()[MOUSE_BTN_1]):
            if(hovered):
                return True
    
    return False