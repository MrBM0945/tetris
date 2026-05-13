from turtle import title

import pygame
import settings

from settings import CELL, BLACK, SHAPE_COLORS

class Renderer:
    def __init__(self, screen): 
        self.screen = screen
        self.title_font = pygame.font.SysFont("arialblack", 60)
     
    def draw_title(self):
        title = "TETRIS"
        
        panel_x = settings.GRID_X + settings.COLS * settings.CELL + 20

        x = panel_x + 60  
        y = 40            
        
        shadow = self.title_font.render(title, True, (0, 0, 0))
        self.screen.blit(shadow, (x + 4, y + 4))

        text = self.title_font.render(title, True, (0, 220, 255))
        self.screen.blit(text, (x, y))

    def adjust_color(self, color, amount):
        return tuple(max(0, min(255, c + amount)) for c in color)

    def draw_game_stats(self, start_time_str, duration_str):
        """Відображає час початку та тривалість гри."""
        stats_font = pygame.font.SysFont("comicsans", 25)
        

        base_x = settings.GRID_X + settings.COLS * settings.CELL + 30
        base_y = settings.GRID_Y + 160 

        start_label = stats_font.render(f"Started: {start_time_str}", True, settings.WHITE)
        self.screen.blit(start_label, (base_x, base_y))

        duration_label = stats_font.render(f"Duration: {duration_str}", True, (0, 255, 100))
        self.screen.blit(duration_label, (base_x, base_y + 30))


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

        
            pygame.draw.rect(self.screen, color, rect)

          
            pygame.draw.polygon(self.screen, light, [
                (bx, by),
                (bx + CELL, by),
                (bx + CELL - 4, by + 4),
                (bx + 4, by + 4)
            ])


            pygame.draw.polygon(self.screen, light, [
                (bx, by),
                (bx, by + CELL),
                (bx + 4, by + CELL - 4),
                (bx + 4, by + 4)
            ])

   
            pygame.draw.polygon(self.screen, dark, [
                (bx, by + CELL),
                (bx + CELL, by + CELL),
                (bx + CELL - 4, by + CELL - 4),
                (bx + 4, by + CELL - 4)
            ])

    
            pygame.draw.polygon(self.screen, dark, [
                (bx + CELL, by),
                (bx + CELL, by + CELL),
                (bx + CELL - 4, by + CELL - 4),
                (bx + CELL - 4, by + 4)
            ])

            # рамка
            pygame.draw.rect(self.screen, BLACK, rect, 1)
            
    def draw_ghost_shape(self, shape, color, x, y):
        for block in shape:
            bx = x + block[0] * CELL
            by = y + block[1] * CELL

            rect = pygame.Rect(bx, by, CELL, CELL)

            pygame.draw.rect(self.screen, color, rect)

            pygame.draw.rect(
                self.screen,
                (220, 220, 220),
                rect,
                1
            )

    def draw_grid(self, cols, rows, grid_x, grid_y, grid_bg, grid_line):
        width = cols * CELL
        height = rows * CELL
        
        for i in range(rows):
            shade = int(235 - i * 2)  # зверху світліше
            color = (shade, shade + 10, shade + 20)
            pygame.draw.rect(
                self.screen,
                color,
                (grid_x, grid_y + i * CELL, width, CELL)
            )

        shadow_color = (200, 210, 220)
        pygame.draw.rect(self.screen, shadow_color, (grid_x, grid_y, width, height), 4)

        for x in range(cols):
           if x % 2 == 0:
               pygame.draw.rect(
               self.screen,
               (245, 250, 255),
                (grid_x + x * CELL, grid_y, CELL, height),
               0
        )
               
        for x in range(cols):
            for y in range(rows):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(
                        self.screen,
                        (228, 238, 248),
                        (grid_x + x * CELL, grid_y + y * CELL, CELL, CELL),
                        0
                        
        )
               
        for x in range(cols+1):
            pygame.draw.line(self.screen, grid_line,
                (grid_x + x * CELL, grid_y),
                (grid_x + x * CELL, grid_y + rows * CELL),
                2
        ) 

        for y in range(rows+1):
            pygame.draw.line(self.screen, grid_line,
                (grid_x, grid_y + y * CELL),
                (grid_x + cols * CELL, grid_y + y * CELL),
                2
            )
        

        

        pygame.draw.rect(
            self.screen,
            (120, 150, 180),
            (grid_x, grid_y, width, height),
            3
    )

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