from typing import Dict, List, Tuple

from tetrominoes import TETROMINOES, SHAPE_COLORS

Coordinate = Tuple[int, int]
Color = Tuple[int, int, int]


class Piece:
    """
    Фігура на полі:
    - має тип
    - має позицію
    - має поточний стан повороту
    - вміє рухатися і повертатися
    - вміє повертати список зайнятих клітин
    """

    def __init__(self, x: int, y: int, shape_type: str) -> None:
        if shape_type not in TETROMINOES:
            raise ValueError(f"Unknown shape type: {shape_type}")

        self.x: int = x
        self.y: int = y
        self.shape_type: str = shape_type
        self.rotation: int = 0
        self.color: Color = SHAPE_COLORS[shape_type]

    def __str__(self) -> str:
        return (
            f"Piece(shape_type='{self.shape_type}', "
            f"x={self.x}, y={self.y}, rotation={self.rotation})"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def get_rotation_count(self) -> int:
        """Повертає кількість станів повороту для поточної фігури."""
        return len(TETROMINOES[self.shape_type])

    def get_current_template(self) -> List[Coordinate]:
        """
        Повертає поточний локальний шаблон фігури.
        Наприклад, для T і rotation = 1 поверне другий стан T.
        """
        states = TETROMINOES[self.shape_type]
        return states[self.rotation % len(states)]

    def get_formatted_shape(self) -> List[Coordinate]:
        """
        Повертає абсолютні координати блоків фігури на сітці.
        Саме цей метод зручно використовувати для інтеграції з Board.
        """
        formatted_shape: List[Coordinate] = []

        for dx, dy in self.get_current_template():
            formatted_shape.append((self.x + dx, self.y + dy))

        return formatted_shape

    def move(self, dx: int, dy: int) -> None:
        """Універсальна зміна позиції."""
        self.x += dx
        self.y += dy

    def move_left(self) -> None:
        self.move(-1, 0)

    def move_right(self) -> None:
        self.move(1, 0)

    def move_down(self) -> None:
        self.move(0, 1)

    def move_up(self) -> None:
        self.move(0, -1)

    def rotate(self) -> None:
        """Поворот на один стан вперед."""
        self.rotation = (self.rotation + 1) % self.get_rotation_count()

    def rotate_back(self) -> None:
        """Відкат повороту на один стан назад."""
        self.rotation = (self.rotation - 1) % self.get_rotation_count()

    def set_position(self, x: int, y: int) -> None:
        """Явно встановлює координати фігури."""
        self.x = x
        self.y = y

    def get_state(self) -> Dict[str, object]:
        """Повертає поточний стан фігури у вигляді словника."""
        return {
            "shape_type": self.shape_type,
            "x": self.x,
            "y": self.y,
            "rotation": self.rotation,
            "color": self.color,
            "cells": self.get_formatted_shape(),
        }