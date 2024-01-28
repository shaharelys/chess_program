# control_map.py
from config import *
from square import Square
from chess_piece import ChessPiece
from typing import Optional
from move import Move


class ControlMap:
    """
    This class ensures correctness for the following data structures:
    Square.controlled_by : set[ChessPiece]
    ChessPiece.controlled_squares : set[Square]
    BoardLines.rows / .columns / .diagonal_up_right / .diagonal_down_right : dict[int, set[ChessPiece]]
    """
    def __init__(self):
        self.lines = BoardLines()

    def handle_move(self, move: Move) -> None:
        piece = move.piece
        captured = move.get_captured_piece()
        square_initial = move.square_initial
        square_final = move.square_final
        self.update_lines(piece, captured, square_final)
        affected_pieces = self.get_affected_pieces(square_initial, square_final)

        for affected in affected_pieces:
            self.update_controlled_squares_old(affected)

    @staticmethod
    def update_controlled_squares_old(piece: ChessPiece) -> None:
        """
        Updates the controlled squares for the given piece and the corresponding squares'
        records of controlling pieces. It ensures these are in sync and updated.
        """
        # TODO: See if this method is required
        # old_controlled_squares = piece.controlled_squares.copy()
        piece.update_controlled_squares()
        # for square in piece.controlled_squares:
        #     square.controlled_by.add(piece)
        # for square in old_controlled_squares - piece.controlled_squares:
        #     square.controlled_by.remove(piece)

    def update_lines(self, piece: ChessPiece, captured: Optional[ChessPiece], square_final: Square) -> None:
        self.lines.remove_piece(piece)
        if captured:
            self.lines.remove_piece(captured)
        self.lines.add_piece(piece, square_final)

    def get_affected_pieces(self, square_initial: Square, square_final: Square) -> set[ChessPiece]:
        """
        Returns a set of all pieces that might be affected by a move.
        """
        affected_pieces = set()
        affected_pieces.update(self.lines.collect_in_line_pieces(square_initial))
        affected_pieces.update(self.lines.collect_in_line_pieces(square_final))
        return affected_pieces


class BoardLines:
    def __init__(self):
        self.rows: dict[int, set[ChessPiece]] = {i: set() for i in range(BOARD_SIZE)}
        self.columns: dict[int, set[ChessPiece]] = {i: set() for i in range(BOARD_SIZE)}
        self.diagonals_up_right: dict[int, set[ChessPiece]] = {i: set() for i in range(-(BOARD_SIZE - 1), BOARD_SIZE)}
        self.diagonals_down_right: dict[int, set[ChessPiece]] = {i: set() for i in range(2 * (BOARD_SIZE - 1) + 1)}

    def add_piece(self, piece: ChessPiece, square: Square) -> None:
        row, col = square.position
        self.rows[row].add(piece)
        self.columns[col].add(piece)
        self.diagonals_up_right[col - row].add(piece)
        self.diagonals_down_right[row + col].add(piece)

    def remove_piece(self, piece: ChessPiece) -> None:
        row, col = piece.square.position
        self.rows[row].discard(piece)  # Using discard to avoid KeyError if the piece is not in the set
        self.columns[col].discard(piece)
        self.diagonals_up_right[col - row].discard(piece)
        self.diagonals_down_right[row + col].discard(piece)

    def collect_in_line_pieces(self, square: Square) -> set[ChessPiece]:
        """
        Collects all pieces on the same rows, columns, and diagonals of the given position.
        """
        row, col = square.position
        collected_pieces = set()
        collected_pieces.update(self.rows[row])
        collected_pieces.update(self.columns[col])
        collected_pieces.update(self.diagonals_up_right[col - row])
        collected_pieces.update(self.diagonals_down_right[row + col])
        return collected_pieces
