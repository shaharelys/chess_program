# game_controller.py
from board_manager import BoardManager, BoardSetup
from square import Square
from move import Move, MoveFactory
from chess_piece import ChessPiece, King
from config import *

class GameController:
    def __init__(self):
        self.board_manager = BoardManager(self._initialize_piece_on_board_setup)  # callback method in class signature
        self.move_factory = MoveFactory(self.board_manager)
        self.white_king: King = self.board_manager.white_king
        self.black_king: King = self.board_manager.black_king

    def get_check_status(self, last_move: Move) -> CheckStatus:
        """
        Returns the check status of the game.
        """
        moved_piece = last_move.piece
        opponent_king_square = self.white_king.square if moved_piece.color is Color.BLACK else self.black_king.square

        # Get the threatened squares of the moved piece
        moved_piece_threatened_squares = self.get_threatened_squares(moved_piece)

        if opponent_king_square in moved_piece_threatened_squares:
            return CheckStatus.WHITE_UNDER_CHECK if moved_piece.color is Color.BLACK else CheckStatus.BLACK_UNDER_CHECK

        return CheckStatus.NO_CHECK

    def _get_moves(self, piece: ChessPiece, legal: bool) -> dict[MoveScope, set['Move']]:
        """
        TODO: write this

        Note: ChessPiece.legal_moves: dict[MoveScope, set['Move']]
        """

        if piece is None:
            raise ValueError("'piece' must not be None.")

        collected_moves: dict[MoveScope, set['Move']] = {MoveScope.STEP: set(), MoveScope.CAPTURE: set()}

        hypothetical_moves_final_positions = piece.get_hypothetical_moves_final_positions()

        foo = self.move_factory.create if legal else self.move_factory.create_threatening_move
        for final_position in hypothetical_moves_final_positions:
            move = foo(piece, final_position)

            # None is returned when final position is not board-constrained
            if move is None or move.scope is MoveScope.INVALID:
                continue

            collected_moves[move.scope].add(move)

        return collected_moves

    def get_legal_moves(self, piece: ChessPiece) -> dict[MoveScope, set['Move']]:
        """
        Returns the set of legal moves for this piece.
        """
        return self._get_moves(piece, legal=True)

    def get_threatened_squares(self, piece: ChessPiece) -> set[Square]:
        """
        Returns the set of squares that are threatened by the specified color.
        This is different from the legal moves as a piece might threaten a square without being able to move to it.
        For example, when a piece is pinned.
        """
        threatening_moves = self._get_moves(piece, legal=False)
        return {move.square_final for move_scope_set in threatening_moves.values() for move in move_scope_set}

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
