import sys
import numpy as np
import pygame
from pygame.locals import KEYDOWN, K_q

from GUI.constants import *

# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 600, 400

_VARS = {'surf': False}

def add_piece(board, action, player):
    rack = int(action / 16)
    row = int((action % 16) / 4)
    col = int((action % 16) % 4)

    board[rack][row][col] = player
    
def main():
    pygame.init()  # Initial Setup
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        # drawISO_Grid(origin=(260, -50))
        board = np.zeros([4, 4, 4])
        drawISOCubeGrid(_VARS['surf'], board, origin=(200, -100), cellSize=15)
        pygame.display.update()


def cartToIso(point):
    isoX = point[0] - point[1]
    isoY = (point[0] + point[1])/2
    return [isoX, isoY]

def drawISO_Grid(screen, origin=[0, 0], size=8, cellSize=20, line_width=1):
    hw = cellSize*size
    borderPoints = [cartToIso(origin),
                    cartToIso([origin[0], hw + origin[1]]),
                    cartToIso([hw + origin[0], hw + origin[1]]),
                    cartToIso([hw + origin[0], origin[1]])]
    # Draw border
    pygame.draw.polygon(screen, BLACK, borderPoints, line_width + 1)
    # Draw inner grid :
    for colRow in range(1, size):
        dim = cellSize*colRow
        pygame.draw.line(screen, BLACK,
                         cartToIso([origin[0], origin[1] + dim]),
                         cartToIso([hw + origin[0], origin[1] + dim]), line_width)
        pygame.draw.line(screen, BLACK,
                         cartToIso([origin[0] + dim, origin[1]]),
                         cartToIso([origin[0] + dim, hw + origin[1]]), line_width)


def drawCube(screen, origin, cellSize, color):
    top_points = [
        origin, 
        (origin[0] + cellSize, origin[1]), 
        (origin[0] + cellSize, origin[1] + cellSize),
        (origin[0], origin[1] + cellSize)
    ]

    tr_corner = top_points[1]
    bl_corner = top_points[2]
    br_corner = top_points[3]
    left_side = [
        bl_corner,
        br_corner,
        (br_corner[0] + cellSize, br_corner[1] + cellSize),
        (bl_corner[0] + cellSize, bl_corner[1] + cellSize),
    ]

    right_side = [
        tr_corner,
        bl_corner,
        (bl_corner[0] + cellSize, bl_corner[1] + cellSize),
        (tr_corner[0] + cellSize, tr_corner[1] + cellSize),
    ]

    iso_top = [cartToIso(point) for point in top_points]
    iso_left = [cartToIso(point) for point in left_side]
    iso_right = [cartToIso(point) for point in right_side]


    pygame.draw.polygon(screen, color, iso_left)
    pygame.draw.polygon(screen, color, iso_right)
    pygame.draw.polygon(screen, color, iso_top)

def drawISOCubeGrid(screen, board, origin=[0, 0], size=4, cellSize=20):
    hw = cellSize*size
    spacing = 1.35

    plane_origins = [origin, (origin[0] + hw*spacing, origin[1] + hw*spacing),
              (origin[0] + (hw*2)*spacing, origin[1] + (hw*2)*spacing),  (origin[0] + (hw*3)*spacing, origin[1] + (hw*3)*spacing)]

    rack = size - 1
    for origin in reversed(plane_origins):
        origin_top = (origin[0] - cellSize, origin[1] - cellSize) 
        drawISO_Grid(screen, origin=origin, size=size, cellSize=cellSize)
        
        for row in range(0, size + 1):
            for col in range(0, size + 1):
                dim_y = cellSize*row
                dim_x = cellSize*col
                
                bottom = cartToIso((origin[0] + dim_y, origin[1] + dim_x))
                top = cartToIso((origin_top[0] + dim_y, origin_top[1] + dim_x))

                pygame.draw.line(screen, BLACK, bottom, top, 1)

                if row != size and col != size:
                    if board[rack][col][row] == -1:
                        drawCube(screen, (origin_top[0] + dim_y, origin_top[1] + dim_x), cellSize, BLUE)
                    elif board[rack][col][row] == 1:
                        drawCube(screen, (origin_top[0] + dim_y, origin_top[1] + dim_x), cellSize, RED)        
        rack -= 1 


        drawISO_Grid(screen, origin=origin_top, size=size, cellSize=cellSize, line_width=2)

def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()