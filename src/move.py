# move.py
from config import *


class Move:
    # a data class to hold a move
    def __init__(self, move_type: MoveType, start: tuple[int, int], end: tuple[int, int]):
        self.valid = False
        self.move_type = move_type
        self.start = start
        self.end = end


class ValidateMove:
    def __init__(self, potential_move: Move, piece_type: PieceType):
        self.potential_move = potential_move
        self.is_type_step = potential_move.move_type is MoveType.STEP
        self.is_type_capture = potential_move.move_type is MoveType.CAPTURE
        self.can_jump_over_pieces = (piece_type == PieceType.KNIGHT)
        self.can_step_into_danger = (piece_type != PieceType.KING)

    def is_inbound(self):
        if 0 <= self.potential_move.end[0] < BOARD_SIZE and 0 <= self.potential_move.end[1] < BOARD_SIZE:
            return True
        return False

    def is_enemy_occupied(self):
        # Implement logic to check if the move is occupied by an enemy piece
        pass

    def is_friendly_occupied(self):
        # Implement logic to check if the move is occupied by a friendly piece
        pass

    def is_blocked(self):
        # Implement logic to check if the move path is blocked by another piece
        if self.can_jump_over_pieces:
            return False
        pass

    def is_opens_king_to_check(self):
        # Implement logic to check if the move opens the king to check
        pass

    @property
    def is_valid_move(self):
        if self.is_inbound() \
                and not self.is_friendly_occupied() \
                and not self.is_blocked() \
                and not self.is_opens_king_to_check():
            return True
        return False

    def is_valid_step(self):
        if self.is_type_step and self.is_valid_move and not self.is_enemy_occupied():
            return True
        return False

    def is_valid_capture(self):
        if self.is_type_capture and self.is_valid_move and self.is_enemy_occupied():
            return True
        return False

    def validate(self):
        if self.is_valid_step() or self.is_valid_capture():
            self.potential_move.valid = True
        else:
            self.potential_move.valid = False
        return self.potential_move.valid
