# chess_piece.py
from abc import ABC, abstractmethod
from square import Square
from config import *


class ChessPiece(ABC):
    def __init__(self, piece_type: PieceType, color: Color):
        self.piece_type = piece_type
        self.color = color
        self.square = None

    @abstractmethod
    def _hypothetical_move_deltas(self) -> set[tuple[int, int]]:
        """
        Generates all potential moves deltas for a piece of that type.
        Coordinates represents the delta in position of which it might move to.
        """
        pass

    def _position_delta_to_final_position(self, delta: tuple[int, int]) -> tuple[int, int]:
        """
        Returns the position of the square that is delta away from the current square.
        """
        row, col = self.square.position
        d_row, d_col = delta
        row_f, col_f = row + d_row, col + d_col
        return row_f, col_f

    def _delta_set_to_final_position_set(self, deltas: set[tuple[int, int]]) -> set[tuple[int, int]]:
        """
        Returns the set of positions that are delta away from the current square.
        """
        return {self._position_delta_to_final_position(delta) for delta in deltas}

    def get_hypothetical_moves_final_positions(self) -> set[tuple[int, int]]:
        """
        Returns the set of positions that this piece can step to.
        """
        return self._delta_set_to_final_position_set(self._hypothetical_move_deltas())


class Pawn(ChessPiece):
    def __init__(self, color: Color):
        super().__init__(piece_type=PieceType.PAWN, color=color)

    def _hypothetical_move_deltas(self) -> set[tuple[int, int]]:

        if self.color == Color.WHITE:
            steps = HypotheticalPositionDeltas.PAWN_WHITE

            if self.square.position[0] == 1:
                steps = HypotheticalPositionDeltas.PAWN_WHITE_START
        else:
            steps = HypotheticalPositionDeltas.PAWN_BLACK

            if self.square.position[0] == 6:
                steps = HypotheticalPositionDeltas.PAWN_BLACK_START

        return steps.value


class Knight(ChessPiece):
    def __init__(self, color: Color):
        super().__init__(piece_type=PieceType.KNIGHT, color=color)

    def _hypothetical_move_deltas(self) -> set[tuple[int, int]]:
        return HypotheticalPositionDeltas.KNIGHT.value


class Bishop(ChessPiece):
    def __init__(self, color: Color):
        super().__init__(piece_type=PieceType.BISHOP, color=color)

    def _hypothetical_move_deltas(self) -> set[tuple[int, int]]:
        return HypotheticalPositionDeltas.BISHOP.value


class Rook(ChessPiece):
    def __init__(self, color: Color):
        super().__init__(piece_type=PieceType.ROOK, color=color)

    def _hypothetical_move_deltas(self) -> set[tuple[int, int]]:
        return HypotheticalPositionDeltas.ROOK.value


class Queen(ChessPiece):
    def __init__(self, color: Color):
        super().__init__(piece_type=PieceType.QUEEN, color=color)

    def _hypothetical_move_deltas(self) -> set[tuple[int, int]]:
        return HypotheticalPositionDeltas.QUEEN.value


class King(ChessPiece):
    def __init__(self, color: Color):
        super().__init__(piece_type=PieceType.KING, color=color)

    def _hypothetical_move_deltas(self) -> set[tuple[int, int]]:
        return HypotheticalPositionDeltas.KING.value


class ChessPieceFactory:
    @staticmethod
    def create(piece_type: PieceType, color: Color) -> ChessPiece:
        if piece_type == PieceType.PAWN:
            return Pawn(color)
        elif piece_type == PieceType.KNIGHT:
            return Knight(color)
        elif piece_type == PieceType.BISHOP:
            return Bishop(color)
        elif piece_type == PieceType.ROOK:
            return Rook(color)
        elif piece_type == PieceType.QUEEN:
            return Queen(color)
        elif piece_type == PieceType.KING:
            return King(color)
        else:
            raise ValueError("Invalid piece type")
