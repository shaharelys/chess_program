# game_manager.py
from config import *
from move import Move, MoveFactory
from square import Square
from chess_piece import ChessPiece
from board_manager import BoardManager


class GameManager:
    def __init__(self, board_manager: BoardManager,):
        self.board_manager = board_manager
        self.move_factory = MoveFactory(board_manager)
        self.history: list[Move] = []
        self.current_player = Color.WHITE

    def update_legal_moves(self, piece: ChessPiece) -> None:
        """
        Updates the set of legal moves for this piece.
        ChessPiece.legal_moves: dict[MoveScope, set['Move']]
        """

        for legal_moves_set in piece.legal_moves.values():
            legal_moves_set.clear()

        hypothetical_moves_final_positions = piece.get_hypothetical_moves_final_positions()

        for pose_f in hypothetical_moves_final_positions:
            move = self.move_factory.get_move(piece, pose_f)  # Returns Move, or None if pose_f isn't board constrained

            if move is None:
                continue

            if move.scope == MoveScope.STEP:
                piece.legal_moves[MoveScope.STEP].add(move)
            elif move.scope is MoveScope.CAPTURE:
                piece.legal_moves[MoveScope.CAPTURE].add(move)

