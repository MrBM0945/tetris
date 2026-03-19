"""
Скрипт для тестування логіки ігрового поля (Board);
"""
import logging
import argparse
from typing import List, Tuple

from board import Board
import settings

# Налаштування логера
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class DummyPiece:
    """Заглушка для фігури (Тетроміно) для цілей тестування."""
    def __init__(self, positions: List[Tuple[int, int]], color: Tuple[int, int, int]) -> None:
        self.positions = positions
        self.color = color

    def get_formatted_shape(self) -> List[Tuple[int, int]]:
        return self.positions

class TestSimulation:
    """Клас-симулятор для тестування різних сценаріїв на ігровому полі."""
    
    def __init__(self, cols: int = settings.COLS, rows: int = settings.ROWS) -> None:
        self.board = Board(columns=cols, rows=rows)
        logger.info(f"Створено симуляцію з полем {cols}x{rows}.")

    def _print_board(self) -> None:
        """Виводить поточний стан поля в консоль (графічна імітація)."""
        print("+" + "-" * (self.board.columns * 2) + "+")
        for row in self.board.grid:
            row_str = "|"
            for color in row:
                if color == settings.BG_COLOR:
                    row_str += " ."
                else:
                    row_str += " #"
            row_str += "|"
            print(row_str)
        print("+" + "-" * (self.board.columns * 2) + "+")

    def _lock_piece(self, piece: DummyPiece) -> None:
        """Фіксує фігуру на полі."""
        for pos in piece.get_formatted_shape():
            self.board.locked_positions[pos] = piece.color
        self.board.update_grid()

    def test_placement_and_overlap(self) -> None:
        """Тестує валідність розміщення та колізії (накладання)."""
        logger.info("=== ТЕСТ 1: Перевірка валідності та накладання ===")
        # Розміщуємо фігуру на дні
        p1 = DummyPiece([(0, 19), (1, 19), (2, 19), (3, 19)], (255, 0, 0)) # Лінія внизу
        
        is_valid = self.board.validate_space(p1)
        logger.info(f"Валідність p1 (вільне місце): {is_valid}")
        assert is_valid, "p1 має бути валідним"
        self._lock_piece(p1)
        
        # Намагаємося поставити туди ж
        p2 = DummyPiece([(1, 19), (1, 18)], (0, 255, 0))
        is_valid2 = self.board.validate_space(p2)
        logger.info(f"Валідність p2 (накладання): {is_valid2}")
        assert not is_valid2, "p2 має бути невалідним (зайнято)"

        self._print_board()

    def test_out_of_bounds(self) -> None:
        """Тестує вихід за межі поля."""
        logger.info("=== ТЕСТ 2: Вихід за межі ===")
        # Нижня межа - y=20 (немає такої клітинки при rows=20, індекси 0-19)
        p1 = DummyPiece([(0, 20)], (0, 0, 255))
        is_valid = self.board.validate_space(p1)
        logger.info(f"Валідність виходу за межі: {is_valid}")
        assert not is_valid, "Блок поза межами має бути невалідним (False)"

    def test_clear_lines(self) -> None:
        """Тестує алгоритм очищення повністю заповнених рядків."""
        logger.info("=== ТЕСТ 3: Очищення ліній === ")
        # Заповнюємо весь рядок 18 штучно
        for i in range(self.board.columns):
            self.board.locked_positions[(i, 18)] = (255, 255, 0)
        self.board.update_grid()
        
        logger.info("Поле ПЕРЕД очищенням (нижній рядок [19] має лінію, і передостанній [18] заповнений повністю):")
        self._print_board()
        
        cleared_count = self.board.clear_rows()
        logger.info(f"Очищено {cleared_count} ліній.")
        
        logger.info("Поле ПІСЛЯ очищення (всі верхні блоки мали впасти вниз):")
        self._print_board()

    def run_all(self) -> None:
        """Запускає весь комплекс тестів."""
        logger.info("Початок виконання всіх тестів.")
        self.test_placement_and_overlap()
        self.test_out_of_bounds()
        self.test_clear_lines()
        
        is_over = self.board.check_game_over()
        logger.info(f"Статус гри (Check Game Over): {is_over}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запуск тестів ядра гри Тетріс.")
    parser.add_argument("--cols", type=int, default=settings.COLS, help="Кількість колонок")
    parser.add_argument("--rows", type=int, default=settings.ROWS, help="Кількість рядків")
    args = parser.parse_args()

    simulator = TestSimulation(cols=args.cols, rows=args.rows)
    simulator.run_all()