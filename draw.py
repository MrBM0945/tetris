import pygame
from settings import CELL, BLACK, SHAPE_COLORS

def shape_height(shape):
    return max(block[1] for block in shape) + 1

def shape_width(shape):
    return max(block[0] for block in shape) + 1

def draw_shape(screen, shape, shape_name, x, y):
    color = SHAPE_COLORS.get(shape_name, (200, 200, 200))
    for block in shape:
        rect = (x + block[0]*CELL, y + block[1]*CELL, CELL, CELL)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

def draw_grid(screen, cols, rows, grid_x, grid_y, grid_bg, grid_line):
    pygame.draw.rect(screen, grid_bg, (grid_x, grid_y, cols*CELL, rows*CELL))
    for x in range(cols+1):
        pygame.draw.line(screen, grid_line, (grid_x+x*CELL, grid_y), (grid_x+x*CELL, grid_y+rows*CELL))
    for y in range(rows+1):
        pygame.draw.line(screen, grid_line, (grid_x, grid_y+y*CELL), (grid_x+cols*CELL, grid_y+y*CELL))

def draw_gallery(screen, tetrominoes, start_x, start_y, cols_per_row=4, spacing=20):
    cell_size = 4 * CELL 
    column_width = cell_size + spacing
    row_height = cell_size + spacing

    current_x, current_y = start_x, start_y
    count = 0

    for name, shape in tetrominoes.items():
        draw_shape(screen, shape, name, current_x, current_y)
        
        count += 1
        current_x += column_width

        if count % cols_per_row == 0:
            current_x = start_x
            current_y += row_height