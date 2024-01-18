# chess_piece.py
from abc import ABC, abstractmethod
from config import *


class ChessPiece(ABC):
    def __init__(self, piece_type: PieceType, color: Color, position: tuple[int, int]):
        self.piece_type = piece_type
        self.color = color
        self.position = position

    @abstractmethod
    def potential_steps(self) -> set[tuple[int, int]]:
        """
        Generates all potential steps for a piece of that type.
        A step coordinates represents the delta in position of which it might step at.
        """
        pass

    @abstractmethod
    def potential_captures(self) -> set[tuple[int, int]]:
        """
        Generates all potential captures for a piece of that type.
        A capture coordinates represents the delta in position of which it might capture at.
        By default, we assume captures are the same as steps for most pieces (Pawn overrides this)
        """
        pass


class Pawn(ChessPiece):
    def potential_steps(self) -> set[tuple[int, int]]:
        steps = set()
        if self.color == Color.WHITE:
            steps.add((1, 0))

            if self.position[0] == 1:
                steps.add((2, 0))
        else:
            steps.add((-1, 0))

            if self.position[0] == 6:
                steps.add((-2, 0))

        return steps

    def potential_captures(self) -> set[tuple[int, int]]:
        if self.color == Color.WHITE:
            captures = {(1, 1), (1, -1)}

        else:
            captures = {(-1, 1), (-1, -1)}

        return captures


class MajorChessPiece(ChessPiece):
    """
    A class to represent a major chess piece (Knight, Bishop, Rook, Queen, King)
    """
    @abstractmethod
    def potential_steps(self) -> set[tuple[int, int]]:
        pass

    def potential_captures(self) -> set[tuple[int, int]]:
        return self.potential_steps()


class Knight(MajorChessPiece):
    def potential_steps(self) -> set[tuple[int, int]]:
        return PieceMoves.KNIGHT


class Bishop(MajorChessPiece):
    def potential_steps(self) -> set[tuple[int, int]]:
        return PieceMoves.BISHOP


class Rook(MajorChessPiece):
    def potential_steps(self) -> set[tuple[int, int]]:
        return PieceMoves.ROOK


class Queen(MajorChessPiece):
    def potential_steps(self) -> set[tuple[int, int]]:
        return PieceMoves.QUEEN


class King(MajorChessPiece):
    def potential_steps(self) -> set[tuple[int, int]]:
        return PieceMoves.KING


class ChessPieceFactory:
    @staticmethod
    def create(piece_type: PieceType, color: Color, position: tuple[int, int]):
        if piece_type == PieceType.PAWN:
            return Pawn(piece_type, color, position)
        elif piece_type == PieceType.KNIGHT:
            return Knight(piece_type, color, position)
        elif piece_type == PieceType.BISHOP:
            return Bishop(piece_type, color, position)
        elif piece_type == PieceType.ROOK:
            return Rook(piece_type, color, position)
        elif piece_type == PieceType.QUEEN:
            return Queen(piece_type, color, position)
        elif piece_type == PieceType.KING:
            return King(piece_type, color, position)
        else:
            raise ValueError("Invalid piece type")
