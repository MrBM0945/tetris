"""
Невеликий тестовий файл для перевірки Piece без pygame.
"""

from piece_factory import create_random_piece, create_piece


def print_piece_info(title: str, piece) -> None:
    print(title)
    print(piece)
    print("Cells:", piece.get_formatted_shape())
    print("State:", piece.get_state())
    print("-" * 40)


def main() -> None:
    piece = create_random_piece()
    print_piece_info("Random piece", piece)

    piece.move_left()
    print_piece_info("After move_left()", piece)

    piece.move_down()
    print_piece_info("After move_down()", piece)

    piece.rotate()
    print_piece_info("After rotate()", piece)

    t_piece = create_piece("T", 5, 2)
    print_piece_info("Manual T piece", t_piece)

    t_piece.rotate()
    t_piece.rotate()
    print_piece_info("T piece after 2 rotations", t_piece)


if __name__ == "__main__":
    main()