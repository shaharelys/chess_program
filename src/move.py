# move.py
from config import *
from chess_piece import *
from square import Square
from typing import Optional


class Move:
    def __init__(self, piece: ChessPiece, move_scope: MoveScope, square_final: Square):
        self.piece = piece
        self.scope = move_scope
        self.square_initial = piece.square
        self.square_final = square_final
        self.captured_piece = square_final.occupant

    @property
    def is_legal(self) -> bool:
        """
        Returns true if the move is legal.
        Note, 'MoveScope.LEGAL' is not included because it's only an intermediate scope state and not a sink state.
        """
        return self.scope is MoveScope.STEP or self.scope is MoveScope.CAPTURE


class MoveValidation:
    def __init__(self, board_manager: 'BoardManager'):
        self.board_manager = board_manager

    @staticmethod
    def _get_line_type(initial_position: tuple[int, int], final_position: tuple[int, int]) -> LineType:
        if initial_position[0] == final_position[0]:
            return LineType.ROW
        if initial_position[1] == final_position[1]:
            return LineType.COLUMN
        if initial_position[0] - initial_position[1] == final_position[0] - final_position[1]:
            return LineType.DIAGONAL_RIGHT_UP
        if initial_position[0] + initial_position[1] == final_position[0] + final_position[1]:
            return LineType.DIAGONAL_RIGHT_DOWN
        else:
            return LineType.INVALID

    def _get_move_line_type(self, move: Move) -> LineType:
        if isinstance(move.piece, Knight):
            return LineType.KNIGHT_MOVE
        return self._get_line_type(move.square_initial.position, move.square_final.position)

    def process_move(self, move: Move) -> MoveScope:
        """
        Processes the move through various validation checks and updates its scope sequentially.
        Returns the final scope of the move; MoveScope.STEP, ...CAPTURE, or ...INVALID.
        """

        # Assert scope starts at hypothetical
        assert move.scope == MoveScope.HYPOTHETICAL, "A move must start at the hypothetical scope."

        # Check for board constraints
        if not self._is_move_board_constrained(move):
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
        elif isinstance(move.piece, Pawn):
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
    def _is_board_constrained(row: int, col: int) -> bool:
        """
        Returns true if the position is within the board constraints.
        """
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return True
        return False

    def _is_move_board_constrained(self, move: Move) -> bool:
        """
        Returns true if the move is within the board constraints.

        Board-Constrained Move: Filters Hypothetical Moves to only include those
        that are within the boundaries of the chessboard.
        """
        row_f, col_f = move.square_final.position
        return self._is_board_constrained(row_f, col_f)

    def _find_next_piece_in_line(self, king: King, piece: ChessPiece) -> Optional[ChessPiece]:
        """
        This method is a helper function to the _is_revealing_check method.
        It finds the first piece on the common line of the king and a piece attempting a move,
        after the piece attempting a move.
        """

        king_row, king_col = king.square.position
        piece_row, piece_col = piece.square.position

        row_step = self._get_step(king_row, piece_row)
        col_step = self._get_step(king_col, piece_col)

        # Already checked the line between the king and the piece, now starting from the piece onwards
        curr_row, curr_col = piece_row + row_step, piece_col + col_step

        # Iterate outwards from the piece up to the board edge
        while self._is_board_constrained(curr_row, curr_col):
            current_square = self.board_manager.get_square(curr_row, curr_col)
            if current_square.occupant:
                return current_square.occupant

            curr_row += row_step
            curr_col += col_step

        return None

    def _is_clean_line_between_squares(self, square1: Square, square2: Square) -> bool:
        """
        Checks if all squares between two given squares are unoccupied and are in a straight line.
        """

        row1, col1 = square1.position
        row2, col2 = square2.position

        row_step = self._get_step(row1, row2)
        col_step = self._get_step(col1, col2)

        curr_row, curr_col = row1 + row_step, col1 + col_step

        # Iterate through squares between square1 and square2
        while (curr_row, curr_col) != (row2, col2):
            if self.board_manager.is_occupied(curr_row, curr_col):
                return False

            curr_row += row_step
            curr_col += col_step

        return True

    def _is_unobstructed(self, move: Move) -> bool:
        """
        Returns true if the move is unobstructed.

        Unobstructed Move: Considers pieces that may block the path of a move.
        Includes moves up to the first obstructing piece.
        """

        if isinstance(move.piece, (King, Knight, Pawn)):
            return True  # Kings, Knights, and Pawns moves are always unobstructed

        square_i, square_f = move.square_initial, move.square_final
        return self._is_clean_line_between_squares(square_i, square_f)

    @staticmethod
    def _get_step(start: int, end: int) -> int:
        """
        Returns the needed step is a line direction between two index values of two rows or columns.
        """
        return 1 if start < end else -1 if start > end else 0

    def _is_revealing_check(self, move: Move) -> bool:
        """
        Determines if a move exposes the king to a check.
        It checks if the moving piece is in line with the king and
        if removing it would open up a line of attack from an opposing piece.
        """

        my_color = move.piece.color
        my_king_ref = self.board_manager.white_king_ref if my_color is Color.WHITE \
            else self.board_manager.black_king_ref
        common_line_type = self._get_line_type(move.square_initial.position, my_king_ref.square.position)

        # Check if the king and the piece do not have a common line.
        if common_line_type is LineType.INVALID:
            return False

        # Check if the piece moves along the common line with the king
        if common_line_type == self._get_move_line_type(move):
            return False

        # Check if there is another piece between the king and the piece
        square1, square2 = my_king_ref.square, move.square_initial  # Starting from the king may be more efficient
        if not self._is_clean_line_between_squares(square1, square2):
            return False

        # Find the first piece 'after' the piece (from the king perspective) along the line
        next_piece_in_line = self._find_next_piece_in_line(my_king_ref, move.piece)

        # If no next piece in line
        if next_piece_in_line is None:
            return False

        # If next piece in line is a friend
        if next_piece_in_line.color == my_color:
            return False

        # If next piece type cannot move to my square by definition
        if isinstance(next_piece_in_line, (King, Knight, Pawn)):
            return False

        if isinstance(next_piece_in_line, Rook) and common_line_type in [LineType.ROW, LineType.COLUMN]:
            return True

        if isinstance(next_piece_in_line, Bishop) \
                and common_line_type in [LineType.DIAGONAL_RIGHT_UP, LineType.DIAGONAL_RIGHT_DOWN]:
            return True

        if isinstance(next_piece_in_line, Queen):
            return True

        raise ValueError("Something went wrong. A piece must be either a King, Knight, Pawn, Rook, Bishop, or Queen.")

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

    def _is_step(self, move: Move) -> bool:
        """
        Returns true if the move is a step.

        Step Move: A subset of Legal Moves that involves moving a piece to an unoccupied square.
        """

        # pawn check
        if isinstance(move.piece, Pawn) and not self._get_move_line_type(move) == LineType.COLUMN:
            return False  # pawns can only step forward on the same column

        return move.square_final.occupant is None

    def _is_capture(self, move: Move) -> bool:
        """
        Returns true if the move is a capture.

        Capture Move: A subset of Legal Moves that involves taking an opponent's piece.
        """

        # pawn check
        if isinstance(move.piece, Pawn) \
                and self._get_move_line_type(move) not in [LineType.DIAGONAL_RIGHT_UP, LineType.DIAGONAL_RIGHT_DOWN]:
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

        assert position_final in piece.get_hypothetical_moves_final_positions(), \
            "Final position must be in the set of that piece's hypothetical final positions."

        square_final = self._get_square_final_if_exists(position_final)

        if square_final is None:
            return None

        move = Move(piece, MoveScope.HYPOTHETICAL, square_final)
        self.validation.process_move(move)  # this sets the scope of the move
        return move  # this can return Invalid moves
