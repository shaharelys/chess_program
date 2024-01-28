# move.py
from config import *
import chess_piece
from chess_piece import ChessPiece
from square import Square


class Move:
    def __init__(self, piece: ChessPiece, move_scope: MoveScope, square_final: Square):
        self.piece = piece
        self.scope = move_scope
        self.square_initial = piece.square
        self.square_final = square_final
        self.captured_piece = square_final.occupant
        self.line_type: MoveLineType = self.get_line_type()  # TODO see if this is needed..

    def _is_knight_move(self) -> bool:
        return isinstance(self.piece, chess_piece.Knight)

    def _is_row_move(self) -> bool:
        return self.square_initial.position[0] == self.square_final.position[0]

    def _is_column_move(self) -> bool:
        return self.square_initial.position[1] == self.square_final.position[1]

    def _is_diagonal_up_right_move(self) -> bool:
        return self.square_initial.position[0] - self.square_initial.position[1] \
            == self.square_final.position[0] - self.square_final.position[1]

    def _is_diagonal_down_right_move(self) -> bool:
        return self.square_initial.position[0] + self.square_initial.position[1] \
            == self.square_final.position[0] + self.square_final.position[1]

    def get_line_type(self) -> MoveLineType:
        if self._is_knight_move():
            return MoveLineType.KNIGHT_MOVE
        if self._is_row_move():
            return MoveLineType.ROW
        if self._is_column_move():
            return MoveLineType.COLUMN
        if self._is_diagonal_up_right_move():
            return MoveLineType.DIAGONAL_RIGHT_UP
        if self._is_diagonal_down_right_move():
            return MoveLineType.DIAGONAL_RIGHT_DOWN


class MoveValidation:
    def __init__(self, board_manager: 'BoardManager'):
        self.board_manager = board_manager

    def process_move(self, move: Move) -> MoveScope:
        """
        Processes the move through various validation checks and updates its scope sequentially.
        :return: The final scope of the move; MoveScope.STEP, ...CAPTURE, or ...INVALID.
        """

        # Assert scope starts at hypothetical
        assert move.scope == MoveScope.HYPOTHETICAL, "A move must start at the hypothetical scope."

        # Check for board constraints
        if not self._is_board_constrained(move):
            self._change_scope_safely(move, MoveScope.INVALID)
            return MoveScope.INVALID
        self._change_scope_safely(move, MoveScope.BOARD_CONSTRAINED)

        # Check for obstructions
        if not self._is_unobstructed(move):
            self._change_scope_safely(move, MoveScope.INVALID)
            return MoveScope.INVALID
        self._change_scope_safely(move, MoveScope.UNOBSTRUCTED)

        # Check for legality
        if not self._is_legal(move):
            self._change_scope_safely(move, MoveScope.INVALID)
            return MoveScope.INVALID
        self._change_scope_safely(move, MoveScope.LEGAL)

        # Final checks for step or capture
        if self._is_step(move):
            self._change_scope_safely(move, MoveScope.STEP)
        elif self._is_capture(move):
            self._change_scope_safely(move, MoveScope.CAPTURE)
        elif isinstance(move.piece, chess_piece.Pawn):
            self._change_scope_safely(move, MoveScope.INVALID)
            return MoveScope.INVALID
        else:
            raise ValueError("Something went wrong. A legal move must be either a step or a capture.")

        return move.scope

    @staticmethod
    def _change_scope_safely(move: Move, new_scope: MoveScope) -> None:
        """
        Changes the scope of the move.
        """
        if new_scope not in ALLOWED_MOVE_SCOPE_TRANSITIONS[move.scope]:
            raise ValueError("A move scope can only transition to a subset of scopes.")

        move.scope = new_scope

    @staticmethod
    def _is_board_constrained(move: Move) -> bool:
        """
        Returns true if the move is within the board constraints.

        Board-Constrained Move: Filters Hypothetical Moves to only include those
        that are within the boundaries of the chessboard.
        """
        row_f, col_f = move.square_final.position
        if 0 <= row_f < BOARD_SIZE and 0 <= col_f < BOARD_SIZE:
            return True
        return False

    def _is_unobstructed(self, move: Move) -> bool:
        """
        Returns true if the move is unobstructed.

        Unobstructed Move: Considers pieces that may block the path of a move.
        Includes moves up to the first obstructing piece. This category represents
        the moves that will be visually indicated on the game interface.
        """

        if isinstance(move.piece, chess_piece.Knight) \
                or isinstance(move.piece, chess_piece.Pawn) \
                or isinstance(move.piece, chess_piece.King):
            return True  # Knights, Pawns, and Kings moves are always unobstructed

        row_i, col_i = move.square_initial.position
        row_f, col_f = move.square_final.position

        row_step = self._get_step(row_i, row_f)
        col_step = self._get_step(col_i, col_f)

        row_c, col_c = row_i + row_step, col_i + col_step  # Current position as row_c, col_c

        while (row_c, col_c) != (row_f, col_f):
            if self.board_manager.is_occupied(row_c, col_c):
                return False  # Path is obstructed

            row_c += row_step
            col_c += col_step

        return True

    @staticmethod
    def _get_step(start, end) -> int:
        return 1 if start < end else -1 if start > end else 0

    @staticmethod
    def _is_revealing_check(move: Move) -> bool:
        """
        Returns true if the piece move is revealing its king to a check.
        """
        # Todo
        return False

    @staticmethod
    def _is_landing_on_friend(move: Move) -> bool:
        """
        Returns true if the piece move is landing on a friendly piece.
        """
        to_be_checked = move.square_final.occupant
        if to_be_checked is not None and to_be_checked.color == move.piece.color:
            return True
        return False

    def _is_legal(self, move: Move) -> bool:
        """
        Returns true if the move is legal.

        Legal Move: Includes Unobstructed Moves that don't reveal the king to a check and don't land on a friendly piece.
        """
        return not (self._is_revealing_check(move) or self._is_landing_on_friend(move))

    @staticmethod
    def _is_step(move: Move) -> bool:
        """
        Returns true if the move is a step.

        Step Move: A subset of Legal Moves that involves moving a piece to an unoccupied square.
        """

        # pawn check
        if isinstance(move.piece, chess_piece.Pawn) and not move.line_type == MoveLineType.COLUMN:
            return False  # pawns can only step forward on the same column

        return move.square_final.occupant is None

    @staticmethod
    def _is_capture(move: Move) -> bool:
        """
        Returns true if the move is a capture.

        Capture Move: A subset of Legal Moves that involves taking an opponent's piece.
        """

        # pawn check
        if isinstance(move.piece, chess_piece.Pawn) \
                and not (move.line_type == MoveLineType.DIAGONAL_RIGHT_UP
                         or move.line_type == MoveLineType.DIAGONAL_RIGHT_DOWN):
            return False  # pawns can only capture diagonally

        return move.square_final.occupant is not None


class MoveFactory:
    def __init__(self, board_manager: 'BoardManager'):
        self.board_manager = board_manager
        self.validation = MoveValidation(board_manager)

    def _get_square_final_if_exists(self, position_final: tuple[int, int]) -> Square or None:
        """
        Returns the square object at the final position if it exists.
        """
        row_f, col_f = position_final
        if 0 <= row_f < BOARD_SIZE and 0 <= col_f < BOARD_SIZE:
            return self.board_manager.get_square(row_f, col_f)
        return None

    def create(self, piece: ChessPiece, position_final: tuple[int, int]) -> Move or None:
        """
        Returns a move object with the correct scope if it's board-constrained, otherwise returns None.
        """

        square_final = self._get_square_final_if_exists(position_final)

        if square_final is None:
            return None

        move = Move(piece, MoveScope.HYPOTHETICAL, square_final)

        return self.validation.process_move(move)

