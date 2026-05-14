"""
Налаштування та константи для гри Tetris.
"""
from typing import Tuple

# --- Налаштування екрану та сітки ---
WIDTH: int = 1000
HEIGHT: int = 850
FPS: int = 60

CELL: int = 30  # Розмір однієї клітинки
COLS: int = 12
ROWS: int = 22

# Координати верхнього лівого кута сітки
GRID_X: int = 50
GRID_Y: int = 100

# --- Кольорова палітра ---
BLACK: Tuple[int, int, int] = (40, 40, 40)
WHITE: Tuple[int, int, int] = (255, 255, 255)
BG_COLOR: Tuple[int, int, int] = (0, 0, 0)
GRID_LINE: Tuple[int, int, int] = (180, 200, 220)

# --- Налаштування гри ---
FALL_SPEED: float = 1.2  # Початкова швидкість падіння: клітинок за секунду 
SPEED_INCREASE_INTERVAL: int = 30  # Кожні 30 секунд
SPEED_INCREASE_PERCENT: float = 0.10  # Збільшення на 10%
MAX_FALL_SPEED: float = 2.0  # Максимальна швидкість падіння
SOFT_DROP_MULTIPLIER: float = 8.0 # Множник швидкості при натисканні вниз (soft drop)

