import random
from typing import List, Optional

from piece import Piece
from tetrominoes import TetrominoRegistry


class PieceGenerator:
    """
    Клас відповідає за систему генерації фігур.

    Можливості:
    - створення конкретної фігури
    - генерація фігур через 7-bag randomizer
    - підтримка черги наступних фігур
    - заготовка під hold-механіку
    """

    def __init__(
        self,
        start_x: int = 3,
        start_y: int = 0,
        preview_size: int = 3,
    ) -> None:
        self.start_x: int = start_x
        self.start_y: int = start_y
        self.preview_size: int = preview_size

        self._bag: List[str] = []
        self._queue: List[str] = []

        self._held_shape_type: Optional[str] = None
        self._can_hold: bool = True

        self._fill_queue()

    def _refill_bag(self) -> None:
        """
        Створює новий перемішаний набір усіх базових фігур.
        Це реалізація 7-bag randomizer.
        """
        self._bag = TetrominoRegistry.get_all_shape_types()
        random.shuffle(self._bag)

    def _pop_shape_type(self) -> str:
        """
        Повертає наступний тип фігури з мішка.
        Якщо мішок порожній — створює новий.
        """
        if not self._bag:
            self._refill_bag()

        return self._bag.pop()

    def _fill_queue(self) -> None:
        """
        Дозаповнює чергу наступних фігур до потрібного розміру.
        """
        while len(self._queue) < self.preview_size:
            self._queue.append(self._pop_shape_type())

    def _build_piece(self, shape_type: str) -> Piece:
        """
        Створює об'єкт Piece у стартовій позиції.
        """
        return Piece(self.start_x, self.start_y, shape_type)

    def create_piece(self, shape_type: str) -> Piece:
        """
        Створює фігуру конкретного типу у стартовій позиції.
        """
        if not TetrominoRegistry.has_shape(shape_type):
            raise ValueError(f"Unknown shape type: {shape_type}")

        return self._build_piece(shape_type)

    def get_next_piece(self) -> Piece:
        """
        Повертає наступну фігуру з черги.
        Після цього черга автоматично поповнюється.
        Також після видачі нової фігури знову дозволяється hold.
        """
        shape_type = self._queue.pop(0)
        self._fill_queue()
        self._can_hold = True
        return self._build_piece(shape_type)

    def peek_next_shape_types(self) -> List[str]:
        """
        Повертає список типів фігур, які зараз є в черзі preview.
        """
        return self._queue.copy()

    def set_start_position(self, start_x: int, start_y: int) -> None:
        """
        Змінює стартову позицію для всіх нових фігур.
        """
        self.start_x = start_x
        self.start_y = start_y

    def reset_hold_state(self) -> None:
        """
        Дозволяє знову використовувати hold для поточної фігури.
        """
        self._can_hold = True

    def can_hold(self) -> bool:
        """
        Повертає, чи можна зараз виконати hold.
        """
        return self._can_hold

    def get_held_shape_type(self) -> Optional[str]:
        """
        Повертає тип фігури, що лежить у hold, або None.
        """
        return self._held_shape_type

    def hold_piece(self, current_piece: Piece) -> Piece:
        """
        Реалізує hold-механіку.

        Логіка:
        - якщо hold ще порожній, поточна фігура відкладається,
          а натомість береться наступна з черги;
        - якщо hold уже містить фігуру, відбувається обмін;
        - повторний hold за один spawn заборонений.
        """
        if not self._can_hold:
            return current_piece

        current_shape_type = current_piece.shape_type
        self._can_hold = False

        if self._held_shape_type is None:
            self._held_shape_type = current_shape_type
            return self.get_next_piece()

        swapped_shape_type = self._held_shape_type
        self._held_shape_type = current_shape_type
        return self._build_piece(swapped_shape_type)