"""
Створення нових фігур.
"""

import random

from piece import Piece
from tetrominoes import BASE_SHAPES


def create_random_piece(start_x: int = 3, start_y: int = 0) -> Piece:
    """
    Створює нову випадкову фігуру.

    Args:
        start_x: стартова x-позиція
        start_y: стартова y-позиція

    Returns:
        Piece: нова випадкова фігура
    """
    shape_type = random.choice(BASE_SHAPES)
    return Piece(start_x, start_y, shape_type)


def create_piece(shape_type: str, start_x: int = 3, start_y: int = 0) -> Piece:
    """
    Створює фігуру конкретного типу.

    Args:
        shape_type: один із типів I, O, T, S, Z, J, L
        start_x: стартова x-позиція
        start_y: стартова y-позиція
    """
    return Piece(start_x, start_y, shape_type)