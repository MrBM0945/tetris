from dataclasses import dataclass
from typing import Dict, List, Tuple

Coordinate = Tuple[int, int]
Color = Tuple[int, int, int]
RotationState = List[Coordinate]
RotationStates = List[RotationState]


@dataclass(frozen=True)
class TetrominoDefinition:
    """Опис одного типу тетроміно: назва, колір і всі стани повороту."""
    name: str
    color: Color
    states: RotationStates

    def get_rotation_count(self) -> int:
        """Повертає кількість станів повороту."""
        return len(self.states)

    def get_state(self, rotation: int) -> RotationState:
        """Повертає шаблон фігури для вказаного стану повороту."""
        return self.states[rotation % len(self.states)]


class TetrominoRegistry:
    """Реєстр усіх базових тетріс-фігур."""
    _tetrominoes: Dict[str, TetrominoDefinition] = {
        "I": TetrominoDefinition(
            name="I",
            color=(0, 240, 240),
            states=[
                [(0, 1), (1, 1), (2, 1), (3, 1)],
                [(2, 0), (2, 1), (2, 2), (2, 3)],
            ],
        ),
        "O": TetrominoDefinition(
            name="O",
            color=(240, 240, 0),
            states=[
                [(1, 0), (2, 0), (1, 1), (2, 1)],
            ],
        ),
        "T": TetrominoDefinition(
            name="T",
            color=(160, 0, 240),
            states=[
                [(1, 0), (0, 1), (1, 1), (2, 1)],
                [(1, 0), (1, 1), (2, 1), (1, 2)],
                [(0, 1), (1, 1), (2, 1), (1, 2)],
                [(1, 0), (0, 1), (1, 1), (1, 2)],
            ],
        ),
        "S": TetrominoDefinition(
            name="S",
            color=(0, 240, 0),
            states=[
                [(1, 0), (2, 0), (0, 1), (1, 1)],
                [(1, 0), (1, 1), (2, 1), (2, 2)],
            ],
        ),
        "Z": TetrominoDefinition(
            name="Z",
            color=(240, 0, 0),
            states=[
                [(0, 0), (1, 0), (1, 1), (2, 1)],
                [(2, 0), (1, 1), (2, 1), (1, 2)],
            ],
        ),
        "J": TetrominoDefinition(
            name="J",
            color=(0, 0, 240),
            states=[
                [(0, 0), (0, 1), (1, 1), (2, 1)],
                [(1, 0), (2, 0), (1, 1), (1, 2)],
                [(0, 1), (1, 1), (2, 1), (2, 2)],
                [(1, 0), (1, 1), (0, 2), (1, 2)],
            ],
        ),
        "L": TetrominoDefinition(
            name="L",
            color=(240, 160, 0),
            states=[
                [(2, 0), (0, 1), (1, 1), (2, 1)],
                [(1, 0), (1, 1), (1, 2), (2, 2)],
                [(0, 1), (1, 1), (2, 1), (0, 2)],
                [(0, 0), (1, 0), (1, 1), (1, 2)],
            ],
        ),
    }

    @classmethod
    def get_definition(cls, shape_type: str) -> TetrominoDefinition:
        """Повертає опис фігури за її типом."""
        if shape_type not in cls._tetrominoes:
            raise ValueError(f"Unknown shape type: {shape_type}")
        return cls._tetrominoes[shape_type]

    @classmethod
    def get_all_shape_types(cls) -> List[str]:
        """Повертає список усіх доступних типів фігур."""
        return list(cls._tetrominoes.keys())

    @classmethod
    def has_shape(cls, shape_type: str) -> bool:
        """Перевіряє, чи існує фігура такого типу."""
        return shape_type in cls._tetrominoes