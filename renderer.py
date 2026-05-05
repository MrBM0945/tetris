import pygame
from settings import CELL, BLACK, SHAPE_COLORS

class Renderer:
    def __init__(self, screen): 
        self.screen = screen

    def adjust_color(self, color, amount):
        return tuple(max(0, min(255, c + amount)) for c in color)

    def shape_height(self, shape):
        return max(block[1] for block in shape) + 1

    def shape_width(self, shape):
        return max(block[0] for block in shape) + 1

    def draw_shape(self, shape, color, x, y):
        light = self.adjust_color(color, 40)
        dark = self.adjust_color(color, -40)

        for block in shape:
            bx = x + block[0] * CELL
            by = y + block[1] * CELL

            rect = pygame.Rect(bx, by, CELL, CELL)

            # основа
            pygame.draw.rect(self.screen, color, rect)

            # 🔆 верх
            pygame.draw.polygon(self.screen, light, [
                (bx, by),
                (bx + CELL, by),
                (bx + CELL - 4, by + 4),
                (bx + 4, by + 4)
            ])

            # 🔆 ліва сторона
            pygame.draw.polygon(self.screen, light, [
                (bx, by),
                (bx, by + CELL),
                (bx + 4, by + CELL - 4),
                (bx + 4, by + 4)
            ])

            # 🌑 низ
            pygame.draw.polygon(self.screen, dark, [
                (bx, by + CELL),
                (bx + CELL, by + CELL),
                (bx + CELL - 4, by + CELL - 4),
                (bx + 4, by + CELL - 4)
            ])

            # 🌑 права сторона
            pygame.draw.polygon(self.screen, dark, [
                (bx + CELL, by),
                (bx + CELL, by + CELL),
                (bx + CELL - 4, by + CELL - 4),
                (bx + CELL - 4, by + 4)
            ])

            # рамка
            pygame.draw.rect(self.screen, BLACK, rect, 1)

    def draw_grid(self, cols, rows, grid_x, grid_y, grid_bg, grid_line):
        pygame.draw.rect(self.screen, grid_bg, (grid_x, grid_y, cols * CELL, rows * CELL))
        for x in range(cols+1):
            pygame.draw.line(self.screen, grid_line, (grid_x+ x * CELL, grid_y), (grid_x + x * CELL, grid_y+rows *CELL))
        for y in range(rows+1):
            pygame.draw.line(self.screen, grid_line, (grid_x, grid_y+y*CELL), (grid_x+cols * CELL, grid_y+ y * CELL))

    def draw_gallery(self, tetrominoes, start_x, start_y, cols_per_row=4, spacing=20):
        cell_size = 4 * CELL 
        column_width = cell_size + spacing
        row_height = cell_size + spacing

        current_x, current_y = start_x, start_y
        count = 0

        for name, shape in tetrominoes.items():
            color = SHAPE_COLORS.get(name, (200, 200, 200))
            self.draw_shape(shape, color, current_x, current_y)

            count += 1
            current_x += column_width

            if count % cols_per_row == 0:
                current_x = start_x
                current_y += row_height