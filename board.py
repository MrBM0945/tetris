class Board:
    
    def __init__(self, columns = 10, rows = 20):
        self.columns = columns
        self.rows = rows
        self.locked_positions = {}
        self.grid = self.create_grid()

    def create_grid(self):
        """Створює чисту матрицю кольорів на основі заблокованих позицій"""
        grid = [[(0, 0, 0) for _ in range(self.columns)] for _ in range(self.rows)]
        for (x, y), color in self.locked_positions.items():
            if y >= 0:
                grid[y][x] = color
        return grid

    def update_grid(self):
        """Оновлює ігрову сітку відповідно до поточних заблокованих позицій."""
        self.grid = self.create_grid()

    def validate_space(self, piece):
        """
        Перевіряє, чи знаходиться фігура в межах поля і чи не накладається на інші блоки.
        Припускаємо, що piece має метод get_formatted_shape(), який повертає [(x, y), (x, y), ...]
        """
        # Створюємо список усіх вільних позицій на полі
        accepted_positions = [[(j, i) for j in range(self.columns) if self.grid[i][j] == (0, 0, 0)] for i in range(self.rows)]
        accepted_positions = [pos for sublist in accepted_positions for pos in sublist] # Згладжуємо список

        # Отримуємо координати блоків поточної фігури
        # (Замініть get_formatted_shape() на метод, який використовується у вашому класі Piece)
        formatted = piece.get_formatted_shape()

        for pos in formatted:
            if pos not in accepted_positions:
                # Дозволяємо фігурі знаходитися вище верхньої межі екрану (y < 0) при її появі
                if pos[1] > -1:
                    return False
        return True

    def clear_rows(self):
        """
        Аналог clear_rows(grid, locked) з main.py.
        """
        inc = 0
        ind = -1  # Додано, щоб уникнути попередження лінтера, про яке ви питали раніше

        for i in range(self.rows - 1, -1, -1):
            row = self.grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                ind = i
                for j in range(self.columns):
                    try:
                        del self.locked_positions[(j, i)]
                    except KeyError:
                        continue
                        
        if inc > 0:
            for key in sorted(list(self.locked_positions), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    self.locked_positions[newKey] = self.locked_positions.pop(key)
            
            # Після зсуву обов'язково оновлюємо сітку
            self.update_grid()
            
        return inc  # Повертаємо кількість видалених рядків для підрахунку очок

    def check_game_over(self):
        """
        Перевіряє, чи не досягли заблоковані блоки верхньої межі ігрового поля.
        """
        for (x, y) in self.locked_positions:
            if y < 1:  # Якщо будь-який блок знаходиться на першому рядку або вище
                return True
        return False