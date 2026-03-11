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
        pass

    def validate_space(self, piece):
        pass

    def clear_rows(self):
        pass

    def check_game_over(self):
        pass