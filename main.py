from board import Board

# 1. Створюємо клас-заглушку для фігури (імітуємо piece.py)
class DummyPiece:
    def __init__(self, positions):
        self.positions = positions

    def get_formatted_shape(self):
        """
        У новій версії validate_space очікує, що фігура сама віддасть 
        свої готові координати (x, y) на полі.
        """
        return self.positions

# 2. Функція для красивого виводу поля в консоль
def print_board(board):
    print("+" + "-" * (board.columns * 2) + "+")
    for row in board.grid:
        row_str = "|"
        for color in row:
            if color == (0, 0, 0):
                row_str += " ."  # Порожня клітинка
            else:
                row_str += " #"  # Заповнена клітинка
        row_str += "|"
        print(row_str)
    print("+" + "-" * (board.columns * 2) + "+")


def run_tests():
    print("=== ТЕСТ 1: Створення порожнього поля ===")
    board = Board(columns=10, rows=10) # Зробимо 10x10 для зручності виводу
    print_board(board)

    print("\n=== ТЕСТ 2: Додавання фігури і перевірка валідності ===")
    piece = DummyPiece(positions=[(0, 9), (1, 9), (0, 8), (1, 8)]) 
    p2 = DummyPiece(positions=[(2, 9), (3, 9), (2, 8), (3, 8)])    
    p3 = DummyPiece(positions=[(4, 9), (5, 9), (6, 9), (7, 9)])
    p4 = DummyPiece(positions=[(0, 9), (1, 9), (0, 8), (1, 8)]) # Конфліктує з 1-ю фігурою

    # --- Фігура 1 ---
    print("Валідність розміщення фігури 1:", board.validate_space(piece))
    for pos in piece.get_formatted_shape():
        board.locked_positions[pos] = (255, 0, 0)
    board.update_grid() # Обов'язково оновлюємо сітку, щоб наступні перевірки "бачили" цю фігуру

    # --- Фігура 2 ---
    print("Валідність розміщення фігури 2:", board.validate_space(p2))
    for pos in p2.get_formatted_shape():
        board.locked_positions[pos] = (0, 255, 0)
    board.update_grid()

    # --- Фігура 3 ---
    print("Валідність розміщення фігури 3:", board.validate_space(p3))
    for pos in p3.get_formatted_shape():
        board.locked_positions[pos] = (0, 0, 255)
    board.update_grid()

    # --- Фігура 4 ---
    # Тепер ця перевірка поверне False, оскільки позиції вже зайняті першою фігурою
    is_p4_valid = board.validate_space(p4)
    print("Валідність розміщення фігури 4:", is_p4_valid)
    
    if is_p4_valid:
        for pos in p4.get_formatted_shape():
            board.locked_positions[pos] = (255, 255, 0)
    else:
        print(" -> Фігуру 4 пропущено, місце вже зайняте!")

    board.update_grid()
    print_board(board)
    
    print("\n=== Очищення ліній ===")
    board.clear_rows()
    print_board(board)

if __name__ == "__main__":
    run_tests()