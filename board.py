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
        accepted_positions: List[Tuple[int, int]] = []
        # Розгортаємо генератори у явні цикли для "надійності" та читабельності
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] == settings.BG_COLOR:
                    accepted_positions.append((j, i))

        formatted: List[Tuple[int, int]] = piece.get_formatted_shape()

        for pos in formatted:
            if pos not in accepted_positions:
                # Дозволяємо фігурам зароджуватися трохи вище ігрового поля (y < 0)
                if pos[1] > -1:
                    return False
        return True

    def clear_rows(self) -> int:
        """
        Перевіряє сітку на наявність повністю заповнених рядків, видаляє їх 
        та зсовує всі вищі блоки вниз.
        
        Returns:
            int: Кількість ліній, які були очищені за цей хід.
        """
        cleared_lines_count: int = 0
        last_cleared_row_index: int = -1

        # Йдемо знизу вгору
        for i in range(self.rows - 1, -1, -1):
            row = self.grid[i]
            # Якщо в рядку немає порожніх клітинок, значить він заповнений
            if settings.BG_COLOR not in row:
                cleared_lines_count += 1
                last_cleared_row_index = i
                for j in range(self.columns):
                    try:
                        del self.locked_positions[(j, i)]
                    except KeyError:
                        continue
                        
        if cleared_lines_count > 0:
            # Сортуємо заблоковані позиції за координатою Y і зсуваємо їх вниз
            sorted_positions = sorted(list(self.locked_positions), key=lambda pos: pos[1])[::-1]
            for key in sorted_positions:
                x, y = key
                if y < last_cleared_row_index:
                    new_key = (x, y + cleared_lines_count)
                    self.locked_positions[new_key] = self.locked_positions.pop(key)
            
            self.update_grid()
            
        return cleared_lines_count

    def check_game_over(self) -> bool:
        """
        Перевіряє, чи не досягли заблоковані блоки верхньої межі ігрового поля, 
        що свідчить про завершення гри.
        
        Returns:
            bool: True, якщо гра закінчена, False в іншому випадку.
        """
        for (x, y) in self.locked_positions:
            if y < 1:
                return True
        return False