import pygame
from settings import CELL, BLACK, SHAPE_COLORS

class Renderer:
    def __init__(self, screen): 
        self.screen = screen

    def shape_height(self, shape):
        return max(block[1] for block in shape) + 1

    def shape_width(self, shape):
        return max(block[0] for block in shape) + 1

    def draw_shape(self, shape, shape_name, x, y):
        color = self.SHAPE_COLORS.get(shape_name, (200, 200, 200))
        for block in shape:
            rect = (x + block[0]*self.CELL, y + block[1]*self.CELL, self.CELL, self.CELL)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.BLACK, rect, 2)

    def draw_grid(self, cols, rows, grid_x, grid_y, grid_bg, grid_line):
        pygame.draw.rect(self.screen, grid_bg, (grid_x, grid_y, cols*self.CELL, rows*self.CELL))
        for x in range(cols+1):
            pygame.draw.line(self.screen, grid_line, (grid_x+x*self.CELL, grid_y), (grid_x+x*self.CELL, grid_y+rows*self.CELL))
        for y in range(rows+1):
            pygame.draw.line(self.screen, grid_line, (grid_x, grid_y+y*self.CELL), (grid_x+cols*self.CELL, grid_y+y*self.CELL))

    def draw_gallery(self, tetrominoes, start_x, start_y, cols_per_row=4, spacing=20):
        cell_size = 4 * CELL 
        column_width = cell_size + spacing
        row_height = cell_size + spacing

        current_x, current_y = start_x, start_y
        count = 0
        for name, shape in tetrominoes.items():
            self.draw_shape(shape, name, current_x, current_y)
        
            count += 1
            current_x += column_width

            if count % cols_per_row == 0:
                current_x = start_x
                current_y += row_height