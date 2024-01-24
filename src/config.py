# config.py

from enum import Enum

BOARD_SIZE = 8


class Color(Enum):
    """Color of a chess piece or a board square."""
    WHITE = 0
    BLACK = 1


class PieceType(Enum):
    PAWN = ('P', 0)
    KNIGHT = ('N', 1)
    BISHOP = ('B', 2)
    ROOK = ('R', 3)
    QUEEN = ('Q', 4)
    KING = ('K', 5)

    def __init__(self, symbol, order):
        self.symbol = symbol
        self.order = order


class InitPiece(Enum):
    """
    Enum representing the initial information of a chess piece
    """
    PAWN_WHITE = PieceType.PAWN, Color.WHITE, [(1, i) for i in range(BOARD_SIZE)]
    PAWN_BLACK = PieceType.PAWN, Color.BLACK, [(6, i) for i in range(BOARD_SIZE)]
    KNIGHT_WHITE = PieceType.KNIGHT, Color.WHITE, [(0, 1), (0, 6)]
    KNIGHT_BLACK = PieceType.KNIGHT, Color.BLACK, [(7, 1), (7, 6)]
    BISHOP_WHITE = PieceType.BISHOP, Color.WHITE, [(0, 2), (0, 5)]
    BISHOP_BLACK = PieceType.BISHOP, Color.BLACK, [(7, 2), (7, 5)]
    ROOK_WHITE = PieceType.ROOK, Color.WHITE, [(0, 0), (0, 7)]
    ROOK_BLACK = PieceType.ROOK, Color.BLACK, [(7, 0), (7, 7)]
    QUEEN_WHITE = PieceType.QUEEN, Color.WHITE, [(0, 3)]
    QUEEN_BLACK = PieceType.QUEEN, Color.BLACK, [(7, 3)]
    KING_WHITE = PieceType.KING, Color.WHITE, [(0, 4)]
    KING_BLACK = PieceType.KING, Color.BLACK, [(7, 4)]

    def __init__(self, piece_type, color, positions):
        self.piece_type = piece_type
        self.positions = positions
        self.color = color


class MoveScope(Enum):
    """
    Enum representing different scopes of a single chess move.
    """
    HYPOTHETICAL_MOVE = 0
    """
    Hypothetical Move: Represents all conceivable moves a piece can make, 
    regardless of the rules of the game or the board's current state.
    """

    BOARD_CONSTRAINED_MOVE = 1
    """
    Board-Constrained Move: Filters Hypothetical Moves to only include those 
    that are within the boundaries of the chessboard.
    """

    UNOBSTRUCTED_MOVE = 2
    """
    Unobstructed Move: Considers pieces that may block the path of a move. 
    Includes moves up to the first obstructing piece. This category represents 
    the moves that will be visually indicated on the game interface.
    """

    ILLEGAL_MOVE = 3
    """
    Illegal Move: Includes Unobstructed Moves that reveal the king to a check or land on a friendly piece.
    """

    LEGAL_MOVE = 4
    """
    Legal Move: Includes Unobstructed Moves that don't reveal the king to a check and don't land on a friendly piece.
    """

    STEP_MOVE = 5
    """
    Step Move: A subset of Legal Moves that involves moving a piece to an unoccupied square.
    """

    CAPTURE_MOVE = 6
    """
    Capture Move: A subset of Legal Moves that involves taking an opponent's piece.
    """


class HypotheticalPositionDeltas(Enum):
    """
    Hypothetical Position Deltas: Represents all conceivable deltas in position a piece can make,
    regardless of the rules of the game or the board's current state.
    """
    # Deltas for class Pawn
    PAWN_WHITE_STEP = {(1, 0)}
    PAWN_BLACK_STEP = {(-1, 0)}
    PAWN_WHITE_START_STEPS = {(2, 0), (1, 0)}
    PAWN_BLACK_START_STEPS = {(-2, 0), (-1, 0)}
    PAWN_WHITE_CAPTURE = {(1, 1), (1, -1)}
    PAWN_BLACK_CAPTURE = {(-1, 1), (-1, -1)}

    # Deltas for class MajorChessPiece (of which steps and captures are the same)
    KNIGHT = {(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)}
    BISHOP = {(i, j) for i in (range(-BOARD_SIZE + 1, BOARD_SIZE - 1)) for j in (i, -i) if i != 0}
    ROOK = {(i, j) for k in (range(-BOARD_SIZE + 1, BOARD_SIZE - 1)) for i, j in ((k, 0), (0, k)) if k != 0}
    QUEEN = {(i, j) for i in (range(-BOARD_SIZE + 1, BOARD_SIZE - 1)) for j in (i, -i) if i != 0}.union(
        {(i, j) for k in (range(-BOARD_SIZE + 1, BOARD_SIZE - 1)) for i, j in ((k, 0), (0, k)) if k != 0})
    KING = {(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)}

