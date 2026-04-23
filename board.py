"""
Модуль, що містить логіку ігрового поля для Тетрісу.
"""
from typing import Dict, List, Tuple, Any
import settings

class GridBoundaryError(Exception):
    """Викликається, коли відбувається спроба вийти за межі ігрового поля."""
    pass

class PositionOccupiedError(Exception):
    """Викликається, коли відбувається спроба розмістити блок на вже зайнятій клітинці."""
    pass

class Board:
    """
    Головний клас, що представляє ігрове поле (стакан) для Тетрісу.
    Відповідає за зберігання стану сітки, валідацію позицій фігур та алгоритм очищення ліній.
    """
    
    def __init__(self, columns: int = settings.COLS, rows: int = settings.ROWS) -> None:
        """
        Ініціалізує ігрове поле заданих розмірів (за замовчуванням бере з settings).
        """
        self._columns: int = columns
        self._rows: int = rows
        # Словник, де ключ - координати (x, y), а значення - колір блоку RGB
        self.locked_positions: Dict[Tuple[int, int], Tuple[int, int, int]] = {}
        # Двовимірний масив кольорів для відмальовки
        self.grid: List[List[Tuple[int, int, int]]] = self.create_grid()

    @property
    def columns(self) -> int:
        """Повертає кількість колонок на ігровому полі."""
        return self._columns

    @property
    def rows(self) -> int:
        """Повертає кількість рядків на ігровому полі."""
        return self._rows

    def __str__(self) -> str:
        """Рядкове представлення об'єкта Board."""
        return f"Board(columns={self.columns}, rows={self.rows}, locked_blocks={len(self.locked_positions)})"

    def __repr__(self) -> str:
        """Офіційне рядкове представлення об'єкта Board."""
        return self.__str__()

    def create_grid(self) -> List[List[Tuple[int, int, int]]]:
        """
        Створює чисту матрицю кольорів на основі порожнього фону та заблокованих позицій.
        
        Returns:
            List[List[Tuple[int, int, int]]]: 2D список, що представляє сітку поля,
            де кожна клітинка містить RGB кортеж кольору.
        """
        grid: List[List[Tuple[int, int, int]]] = [[settings.BG_COLOR for _ in range(self.columns)] for _ in range(self.rows)]
        for (x, y), color in self.locked_positions.items():
            if y >= 0:
                grid[y][x] = color
        return grid

    def update_grid(self) -> None:
        """Оновлює внутрішню ігрову сітку відповідно до поточних заблокованих позицій."""
        self.grid = self.create_grid()

    def validate_space(self, piece: Any) -> bool:
        """
        Перевіряє, чи знаходиться запропонована фігура в межах ігрового поля 
        і чи не накладається вона на вже заблоковані блоки.
        
        Args:
            piece: Об'єкт фігури, що має метод get_formatted_shape() -> List[Tuple[int, int]].
            
        Returns:
            bool: True, якщо позиція валідна (вільна), False в іншому випадку.
        """
        for x, y in piece.get_formatted_shape():
            # Фігура може спавнитись вище екрану (y < 0)
            if y < 0:
                # Головне, щоб вона не виходила за ліву/праву стінку
                if x < 0 or x >= self.columns:
                    return False
                continue
                
            # Перевірка на вихід за межі поля (стінки та дно)
            if x < 0 or x >= self.columns or y >= self.rows:
                return False
                
            # Перевірка на зіткнення зі збереженими блоками (пошук у словнику миттєвий)
            if (x, y) in self.locked_positions:
                return False
                
        return True

    def clear_rows(self) -> int:
        """Оптимізоване та правильне очищення рядків."""
        cleared_lines_count: int = 0
        
        row = self.rows - 1
        while row >= 0:
            is_full = all((col, row) in self.locked_positions for col in range(self.columns))
            
            if is_full:
                cleared_lines_count += 1
                
                for col in range(self.columns):
                    del self.locked_positions[(col, row)]

                new_locked = {}
                for (x, y), color in self.locked_positions.items():
                    if y < row:
                        new_locked[(x, y + 1)] = color
                    else:
                        new_locked[(x, y)] = color
                
                self.locked_positions = new_locked
            else:
                row -= 1

        if cleared_lines_count > 0:
            self.update_grid()
            
        return cleared_lines_count

    def check_game_over(self) -> bool:
        """
        Перевіряє, чи не досягли заблоковані блоки верхньої межі ігрового поля, 
        що свідчить про завершення гри.
        
        Returns:
            bool: True, якщо гра закінчена, False в іншому випадку.
        """
        return any(y < 1 for _, y in self.locked_positions)