import pygame
import settings

from settings import CELL, BLACK


class Renderer:
    def __init__(self, screen):
        self.screen = screen

        # --- Кешовані шрифти (створюються один раз) ---
        self.title_font = pygame.font.SysFont("arialblack", 60)
        self.stats_font = pygame.font.SysFont("comicsans", 25)

        # --- Кешований фон сітки (рендериться один раз) ---
        self._grid_surface = self._build_grid_surface(
            settings.COLS, settings.ROWS, settings.GRID_LINE
        )

    # ------------------------------------------------------------------
    # Внутрішні хелпери
    # ------------------------------------------------------------------

    def _build_grid_surface(self, cols: int, rows: int, grid_line) -> pygame.Surface:
        """Будує Surface з намальованою сіткою (фон + лінії).
        Викликається один раз при ініціалізації — дуже дешево під час гри."""
        width = cols * CELL
        height = rows * CELL
        surf = pygame.Surface((width, height))

        # Градієнтний фон: зверху світліше
        for i in range(rows):
            shade = int(235 - i * 2)
            color = (shade, shade + 10, shade + 20)
            pygame.draw.rect(surf, color, (0, i * CELL, width, CELL))

        # Шахова текстура поверх градієнту
        for x in range(cols):
            for y in range(rows):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(surf, (228, 238, 248), (x * CELL, y * CELL, CELL, CELL))

        # Вертикальні лінії
        for x in range(cols + 1):
            pygame.draw.line(surf, grid_line, (x * CELL, 0), (x * CELL, height), 2)

        # Горизонтальні лінії
        for y in range(rows + 1):
            pygame.draw.line(surf, grid_line, (0, y * CELL), (width, y * CELL), 2)

        # Зовнішня рамка
        pygame.draw.rect(surf, (120, 150, 180), (0, 0, width, height), 3)

        return surf

    def adjust_color(self, color, amount):
        return tuple(max(0, min(255, c + amount)) for c in color)

    # ------------------------------------------------------------------
    # Публічні методи малювання
    # ------------------------------------------------------------------

    def draw_title(self):
        title = "TETRIS"
        panel_x = settings.GRID_X + settings.COLS * settings.CELL + 20
        x = panel_x + 60
        y = 40

        shadow = self.title_font.render(title, True, (0, 0, 0))
        self.screen.blit(shadow, (x + 4, y + 4))

        text = self.title_font.render(title, True, (0, 220, 255))
        self.screen.blit(text, (x, y))

    def draw_game_stats(self, start_time_str: str, duration_str: str):
        """Відображає час початку та тривалість гри (шрифт кешований)."""
        base_x = settings.GRID_X + settings.COLS * settings.CELL + 30
        base_y = settings.GRID_Y + 160

        start_label = self.stats_font.render(f"Started: {start_time_str}", True, settings.WHITE)
        self.screen.blit(start_label, (base_x, base_y))

        duration_label = self.stats_font.render(f"Duration: {duration_str}", True, (0, 255, 100))
        self.screen.blit(duration_label, (base_x, base_y + 30))

    def draw_grid(self, grid_x: int, grid_y: int):
        """Малює кешований фон сітки одним blit."""
        self.screen.blit(self._grid_surface, (grid_x, grid_y))

    def draw_shape(self, shape, color, x: int, y: int):
        light = self.adjust_color(color, 40)
        dark = self.adjust_color(color, -40)

        for block in shape:
            bx = x + block[0] * CELL
            by = y + block[1] * CELL
            rect = pygame.Rect(bx, by, CELL, CELL)

            pygame.draw.rect(self.screen, color, rect)

            # Верхній відблиск
            pygame.draw.polygon(self.screen, light, [
                (bx, by), (bx + CELL, by),
                (bx + CELL - 4, by + 4), (bx + 4, by + 4)
            ])
            # Лівий відблиск
            pygame.draw.polygon(self.screen, light, [
                (bx, by), (bx, by + CELL),
                (bx + 4, by + CELL - 4), (bx + 4, by + 4)
            ])
            # Нижня тінь
            pygame.draw.polygon(self.screen, dark, [
                (bx, by + CELL), (bx + CELL, by + CELL),
                (bx + CELL - 4, by + CELL - 4), (bx + 4, by + CELL - 4)
            ])
            # Права тінь
            pygame.draw.polygon(self.screen, dark, [
                (bx + CELL, by), (bx + CELL, by + CELL),
                (bx + CELL - 4, by + CELL - 4), (bx + CELL - 4, by + 4)
            ])

            # Рамка
            pygame.draw.rect(self.screen, BLACK, rect, 1)

    def draw_ghost_shape(self, shape, color, x: int, y: int):
        for block in shape:
            bx = x + block[0] * CELL
            by = y + block[1] * CELL
            rect = pygame.Rect(bx, by, CELL, CELL)

            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (220, 220, 220), rect, 1)