# малювання фігур
import pygame
from settings import CELL, BLACK

def shape_height(shape):
    return max(block[1] for block in shape) + 1

def shape_width(shape):
    return max(block[0] for block in shape) + 1

def draw_shape(screen, shape, x, y):
    for block in shape:
        pygame.draw.rect(
            screen,
            BLACK,
            (x + block[0]*CELL,
             y + block[1]*CELL,
             CELL,
             CELL),
            2
        )

def draw_grid(screen, cols, rows, grid_x, grid_y, grid_bg, grid_line):
    pygame.draw.rect(screen, grid_bg,
                     (grid_x, grid_y, cols*CELL, rows*CELL))
    for x in range(cols+1):
        pygame.draw.line(screen, grid_line,
                         (grid_x+x*CELL, grid_y),
                         (grid_x+x*CELL, grid_y+rows*CELL))
    for y in range(rows+1):
        pygame.draw.line(screen, grid_line,
                         (grid_x, grid_y+y*CELL),
                         (grid_x+cols*CELL, grid_y+y*CELL))

def draw_gallery(screen, tetrominoes, start_x, start_y, cols_per_row=4, spacing=5):
    x, y = start_x, start_y
    max_box_width = max(shape_width(s) for s in tetrominoes) * CELL
    max_box_height = max(shape_height(s) for s in tetrominoes) * CELL
    count = 0

    for shape in tetrominoes:
        shape_w = shape_width(shape) * CELL
        shape_h = shape_height(shape) * CELL
        offset_x = (max_box_width - shape_w)//2
        offset_y = (max_box_height - shape_h)//2
        draw_shape(screen, shape, x + offset_x, y + offset_y)

        x += max_box_width + spacing
        count += 1

        if count % cols_per_row == 0:
            x = start_x
            y += max_box_height + spacing
