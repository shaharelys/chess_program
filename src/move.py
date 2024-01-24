# move.py
from __future__ import annotations
from config import *
from chess_piece import ChessPiece


class Move:
    # a data class to hold a move
    def __init__(self, piece: ChessPiece, move_scope: MoveScope, initial_square: 'Square', final_square: 'Square'):
        self.valid = False
        self.piece = piece
        self.move_type = move_scope
        self.square_initial = initial_square
        self.square_final = final_square

    def get_captured_piece(self) -> ChessPiece or None:
        if self.move_type is MoveType.CAPTURE:
            return self.square_final.occupant
        return None


class ValidateMove:
    def __init__(self, potential_move: Move, piece_type: PieceType):
        self.potential_move = potential_move
        self.is_type_step = potential_move.move_type is MoveType.STEP
        self.is_type_capture = potential_move.move_type is MoveType.CAPTURE
        self.can_jump_over_pieces = (piece_type == PieceType.KNIGHT)
        self.can_step_into_danger = (piece_type != PieceType.KING)

    def is_inbound(self) -> bool:
        final_position = self.potential_move.square_final.position
        if 0 <= final_position[0] < BOARD_SIZE and 0 <= final_position[1] < BOARD_SIZE:
            return True
        return False

    def is_enemy_occupied(self) -> bool:
        # Implement logic to check if the move is occupied by an enemy piece
        pass

    def is_friendly_occupied(self) -> bool:
        # Implement logic to check if the move is occupied by a friendly piece
        pass

    def is_blocked(self) -> bool:
        # Implement logic to check if the move path is blocked by another piece
        if self.can_jump_over_pieces:
            return False
        pass

    def is_opens_king_to_check(self) -> bool:
        # Implement logic to check if the move opens the king to check
        pass

    def is_controlled(self):
        if self.is_inbound() and not self.is_blocked():
            return True
        return False

    @property
    def is_valid_move(self) -> bool:
        if self.is_controlled() and not self.is_friendly_occupied() and not self.is_opens_king_to_check():
            return True
        return False

    def is_valid_step(self) -> bool:
        if self.is_type_step and self.is_valid_move and not self.is_enemy_occupied():
            return True
        return False

    def is_valid_capture(self) -> bool:
        if self.is_type_capture and self.is_valid_move and self.is_enemy_occupied():
            return True
        return False

    def validate(self) -> bool:
        if self.is_valid_step() or self.is_valid_capture():
            self.potential_move.valid = True
        else:
            self.potential_move.valid = False
        return self.potential_move.valid
