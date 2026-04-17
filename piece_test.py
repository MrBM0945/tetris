"""
Тестування модуля Piece для всіх 7 базових тетріс-фігур.
"""
from piece_factory import PieceGenerator
from tetrominoes import TetrominoRegistry


def print_separator() -> None:
    print("-" * 60)


def test_initial_state(shape_type: str) -> None:
    """Перевіряє початковий стан фігури."""
    generator = PieceGenerator(start_x=3, start_y=0)
    piece = generator.create_piece(shape_type)

    print(f"TEST: initial state for {shape_type}")
    print(piece)

    cells = piece.get_formatted_shape()
    print("Cells:", cells)

    assert piece.shape_type == shape_type, f"{shape_type}: wrong shape_type"
    assert piece.x == 3, f"{shape_type}: wrong initial x"
    assert piece.y == 0, f"{shape_type}: wrong initial y"
    assert piece.rotation == 0, f"{shape_type}: wrong initial rotation"
    assert len(cells) == 4, f"{shape_type}: tetromino must contain 4 blocks"

    print("OK")
    print_separator()


def test_movement(shape_type: str) -> None:
    """Перевіряє рух фігури."""
    generator = PieceGenerator(start_x=3, start_y=0)
    piece = generator.create_piece(shape_type)

    print(f"TEST: movement for {shape_type}")
    before = piece.get_formatted_shape()
    print("Before move:", before)

    piece.move_left()
    left_cells = piece.get_formatted_shape()
    print("After move_left():", left_cells)

    piece.move_right()
    piece.move_right()
    right_cells = piece.get_formatted_shape()
    print("After move_right() twice:", right_cells)

    piece.move_down()
    down_cells = piece.get_formatted_shape()
    print("After move_down():", down_cells)

    assert piece.y == 1, f"{shape_type}: wrong y after move_down"

    print("OK")
    print_separator()


def test_rotation_cycle(shape_type: str) -> None:
    """
    Перевіряє, що після повного циклу поворотів
    фігура повертається до початкового стану.
    """
    generator = PieceGenerator(start_x=4, start_y=2)
    piece = generator.create_piece(shape_type)

    print(f"TEST: rotation cycle for {shape_type}")

    initial_cells = piece.get_formatted_shape()
    initial_rotation = piece.rotation
    rotation_count = piece.get_rotation_count()

    print("Initial rotation:", initial_rotation)
    print("Initial cells:", initial_cells)
    print("Rotation count:", rotation_count)

    for _ in range(rotation_count):
        cells = piece.get_formatted_shape()
        print(f"Rotation {piece.rotation}: {cells}")
        piece.rotate()

    final_cells = piece.get_formatted_shape()
    print("After full cycle:", final_cells)

    assert piece.rotation == initial_rotation, (
        f"{shape_type}: rotation did not return to initial state"
    )
    assert final_cells == initial_cells, (
        f"{shape_type}: cells did not return to initial state after full cycle"
    )

    print("OK")
    print_separator()


def test_state_dictionary(shape_type: str) -> None:
    """Перевіряє коректність get_state()."""
    generator = PieceGenerator(start_x=5, start_y=1)
    piece = generator.create_piece(shape_type)

    print(f"TEST: get_state() for {shape_type}")
    state = piece.get_state()
    print("State:", state)

    assert state["shape_type"] == shape_type, f"{shape_type}: wrong state shape_type"
    assert state["x"] == 5, f"{shape_type}: wrong state x"
    assert state["y"] == 1, f"{shape_type}: wrong state y"
    assert state["rotation"] == 0, f"{shape_type}: wrong state rotation"
    assert len(state["cells"]) == 4, f"{shape_type}: state cells must contain 4 blocks"

    print("OK")
    print_separator()


def test_rotation_count(shape_type: str) -> None:
    """Перевіряє, що кількість станів повороту відповідає опису фігури в реєстрі."""
    generator = PieceGenerator(start_x=0, start_y=0)
    piece = generator.create_piece(shape_type)

    print(f"TEST: rotation count for {shape_type}")
    expected_count = TetrominoRegistry.get_definition(shape_type).get_rotation_count()
    actual_count = piece.get_rotation_count()

    print("Expected:", expected_count)
    print("Actual:", actual_count)

    assert actual_count == expected_count, f"{shape_type}: wrong rotation count"

    print("OK")
    print_separator()


def run_all_tests() -> None:
    """Запускає всі тести для всіх фігур."""
    print("STARTING ALL PIECE TESTS")
    print("=" * 60)

    for shape_type in TetrominoRegistry.get_all_shape_types():
        test_initial_state(shape_type)
        test_movement(shape_type)
        test_rotation_count(shape_type)
        test_rotation_cycle(shape_type)
        test_state_dictionary(shape_type)

    print("ALL TESTS PASSED SUCCESSFULLY")


if __name__ == "__main__":
    run_all_tests()