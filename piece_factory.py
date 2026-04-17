import random

from piece import Piece
from tetrominoes import TetrominoRegistry


def create_random_piece(start_x: int = 3, start_y: int = 0) -> Piece:
    """
    Створює нову випадкову фігуру.
    """
    shape_type = random.choice(TetrominoRegistry.get_all_shape_types())
    return Piece(start_x, start_y, shape_type)


def create_piece(shape_type: str, start_x: int = 3, start_y: int = 0) -> Piece:
    """
    Створює фігуру конкретного типу.
    """
    return Piece(start_x, start_y, shape_type)