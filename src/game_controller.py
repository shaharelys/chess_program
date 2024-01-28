# game_controller.py
from board_manager import BoardManager, BoardSetup
from square import Square
from move import Move, MoveFactory
from chess_piece import ChessPiece
from config import *


class GameController:
    def __init__(self):
        self.board_manager = BoardManager(self._initialize_piece_on_board_setup)  # callback method in class signature
        self.move_factory = MoveFactory(self.board_manager)

    def get_legal_moves(self, piece: ChessPiece) -> dict[MoveScope, set['Move']]:
        """
        Updates the set of legal moves for this piece.
        Note: ChessPiece.legal_moves: dict[MoveScope, set['Move']]
        """
        legal_moves: dict[MoveScope, set['Move']] = {MoveScope.STEP: set(), MoveScope.CAPTURE: set()}

        if piece is None:
            raise ValueError("'piece' must not be None.")

        hypothetical_moves_final_positions = piece.get_hypothetical_moves_final_positions()

        for final_position in hypothetical_moves_final_positions:
            move = self.move_factory.create(piece, final_position)

            # None is returned when final position is not board-constrained
            if move is None or move.scope is MoveScope.INVALID:
                continue

            legal_moves[move.scope].add(move)

        return legal_moves

    @staticmethod
    def _set_piece(piece: ChessPiece, square: Square):
        """
        Place a piece on this square.
        """
        assert piece.square is None, "Piece must be removed from its current square before being placed on another."
        assert square.occupant is None, "Square must be void before placing a piece on it."

        piece.square = square
        square.occupant = piece

    def _initialize_piece_on_board_setup(self, piece: ChessPiece, square: Square, caller: BoardSetup):
        """
        This method is called on initialization by BoardSetup as callback.
        It sets 'piece' on 'square' and updates the piece's legal moves.
        """
        assert isinstance(caller, BoardSetup), "'caller' must be of type 'BoardSetup'."

        self._set_piece(piece, square)

    @staticmethod
    def _remove_piece(piece: ChessPiece, square: Square):
        """
        Remove the piece occupying the square.
        """
        assert square.occupant is piece, "'square.occupant' must refer to the specified 'piece' to be removed."
        assert piece.square is square, "'piece.square' must refer to the specified 'square' to be removed from."
        piece.square = None
        square.occupant = None

    def _initiate_step_move(self, move: Move) -> None:
        """
        Initiates a step move.
        """
        assert move.scope == MoveScope.STEP, "'move' must be of type 'STEP'."

        piece = move.piece
        square_i, square_f = move.square_initial, move.square_final

        self._remove_piece(piece, square_i)
        self._set_piece(piece, square_f)

    def _initiate_capture_move(self, move: Move) -> None:
        """
        Initiates a capture move.
        """
        assert move.scope == MoveScope.CAPTURE, "'move' must be of type 'CAPTURE'."

        piece, captured_piece = move.piece, move.captured_piece
        square_i, square_f = move.square_initial, move.square_final

        self._remove_piece(piece, square_i)
        self._remove_piece(captured_piece, square_f)
        self._set_piece(piece, square_f)

    def _initiate_move(self, move: Move) -> None:
        """
        Initiates a move.
        """
        if move.scope == MoveScope.STEP:
            self._initiate_step_move(move)
        elif move.scope == MoveScope.CAPTURE:
            self._initiate_capture_move(move)
        else:
            raise ValueError(f"Invalid move scope: {move.scope}")

    def initiate_move_and_related_methods(self, move: Move) -> None:
        """
        initiates a move while supporting private related operations.
        """
        self._initiate_move(move)
        # add related methods here
