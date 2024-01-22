# chess_piece.py
from abc import ABC, abstractmethod
from config import *
from square import Square


class ChessPiece(ABC):
    def __init__(self, piece_type: PieceType, color: Color, position: tuple[int, int]):
        self.piece_type = piece_type
        self.color = color
        self.position = position
        self.controlled_squares: set[Square] = set()

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
        """
        pass

    @abstractmethod
    def update_controlled_squares(self) -> None:
        """
        Updates the set of squares controlled by this piece.
        """
        pass


class Pawn(ChessPiece):

    def __init__(self, color: Color, position: tuple[int, int]):
        super().__init__(piece_type=PieceType.PAWN, color=color, position=position)

    def potential_steps(self) -> set[tuple[int, int]]:

        if self.color == Color.WHITE:
            steps = HypotheticalPositionDeltas.PAWN_WHITE_STEP

            if self.position[0] == 1:
                steps = HypotheticalPositionDeltas.PAWN_WHITE_START_STEPS
        else:
            steps = HypotheticalPositionDeltas.PAWN_BLACK_STEP

            if self.position[0] == 6:
                steps = HypotheticalPositionDeltas.PAWN_BLACK_START_STEPS

        return steps.value

    def potential_captures(self) -> set[tuple[int, int]]:
        if self.color == Color.WHITE:
            captures = HypotheticalPositionDeltas.PAWN_WHITE_CAPTURE

        else:
            captures = HypotheticalPositionDeltas.PAWN_BLACK_CAPTURE

        return captures.value


class MajorChessPiece(ChessPiece):
    """
    A class to represent a major chess piece (Knight, Bishop, Rook, Queen, King)
    By default, we assume captures are the same as steps for most pieces (Pawn is an exception)
    """
    @abstractmethod
    def potential_steps(self) -> set[tuple[int, int]]:
        pass

    def potential_captures(self) -> set[tuple[int, int]]:
        return self.potential_steps()


class Knight(MajorChessPiece):
    def __init__(self, color: Color, position: tuple[int, int]):
        super().__init__(piece_type=PieceType.KNIGHT, color=color, position=position)

    def potential_steps(self) -> set[tuple[int, int]]:
        return HypotheticalPositionDeltas.KNIGHT.value


class Bishop(MajorChessPiece):
    def __init__(self, color: Color, position: tuple[int, int]):
        super().__init__(piece_type=PieceType.BISHOP, color=color, position=position)

    def potential_steps(self) -> set[tuple[int, int]]:
        return HypotheticalPositionDeltas.BISHOP.value


class Rook(MajorChessPiece):
    def __init__(self, color: Color, position: tuple[int, int]):
        super().__init__(piece_type=PieceType.ROOK, color=color, position=position)

    def potential_steps(self) -> set[tuple[int, int]]:
        return HypotheticalPositionDeltas.ROOK.value


class Queen(MajorChessPiece):
    def __init__(self, color: Color, position: tuple[int, int]):
        super().__init__(piece_type=PieceType.QUEEN, color=color, position=position)

    def potential_steps(self) -> set[tuple[int, int]]:
        return HypotheticalPositionDeltas.QUEEN.value


class King(MajorChessPiece):
    def __init__(self, color: Color, position: tuple[int, int]):
        super().__init__(piece_type=PieceType.KING, color=color, position=position)

    def potential_steps(self) -> set[tuple[int, int]]:
        return HypotheticalPositionDeltas.KING.value


class ChessPieceFactory:
    @staticmethod
    def create(piece_type: PieceType, color: Color, position: tuple[int, int]) -> ChessPiece:
        if piece_type == PieceType.PAWN:
            return Pawn(color, position)
        elif piece_type == PieceType.KNIGHT:
            return Knight(color, position)
        elif piece_type == PieceType.BISHOP:
            return Bishop(color, position)
        elif piece_type == PieceType.ROOK:
            return Rook(color, position)
        elif piece_type == PieceType.QUEEN:
            return Queen(color, position)
        elif piece_type == PieceType.KING:
            return King(color, position)
        else:
            raise ValueError("Invalid piece type")
