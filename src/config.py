# config.py

from enum import Enum

BOARD_SIZE = 8


class Color(Enum):
    """Color of a chess piece or a board square."""
    WHITE = 0
    BLACK = 1


class PieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5


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

