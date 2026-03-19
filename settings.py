"""
Налаштування та константи для гри Tetris.
"""
from typing import Tuple

# Розміри ігрового поля (в блоках)
COLS: int = 10
ROWS: int = 20

# Розміри одного блоку (в пікселях)
BLOCK_SIZE: int = 30

# Кольори екрану та сітки
BG_COLOR: Tuple[int, int, int] = (0, 0, 0)
GRID_COLOR: Tuple[int, int, int] = (128, 128, 128)

# Швидкість гри
FPS: int = 60
FALL_SPEED: float = 0.5
