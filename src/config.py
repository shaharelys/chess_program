# config.py

from enum import Enum

BOARD_SIZE = 8


class Color(Enum):
    WHITE = 1
    BLACK = 2


class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class MoveType(Enum):
    STEP = 1
    CAPTURE = 2


class PieceMoves(Enum):
    KNIGHT = {(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)}
    BISHOP = {(i, j) for i in (range(-BOARD_SIZE + 1, BOARD_SIZE - 1)) for j in (i, -i) if i != 0}
    ROOK = {(i, j) for k in (range(-BOARD_SIZE + 1, BOARD_SIZE - 1)) for i, j in ((k, 0), (0, k)) if k != 0}
    QUEEN = BISHOP.value.union(ROOK.value)
    KING = {(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)}

