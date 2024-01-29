# game_manager.py
"""
Manages a single game logic, including move processing, game state maintenance, and enforcing rules.
"""
from config import *
from game_controller import GameController
from move import Move
from chess_piece import ChessPiece, King


class GameManager:
    def __init__(self):
        self.controller = GameController()
        self.board_manager = self.controller.board_manager
        self.history: list[Move] = []
        self.current_player_color = Color.WHITE
        self.piece_type_board_state = None
        self._update_piece_type_board_state()
        self.white_king_ref: King = self.get_king_ref(Color.WHITE)
        self.black_king_ref: King = self.get_king_ref(Color.BLACK)

    def get_king_ref(self, color: Color) -> King:
        """
        Returns the king's reference at the beginning of the game.
        """
        row, col = InitPiece.KING_WHITE.positions[0] if color is Color.WHITE else InitPiece.KING_BLACK.positions[0]
        return self.board_manager.get_square(row, col).occupant

    def _update_history(self, move: Move) -> None:
        """
        Updates the history of moves.
        """
        self.history.append(move)

    def _update_current_player(self) -> None:
        """
        Updates the current player.
        """
        self.current_player_color = Color.WHITE if self.current_player_color == Color.BLACK else Color.BLACK

    def _update_on_move(self, move: Move) -> None:
        """
        Updates the game state after a move has been made.
        """
        self._update_history(move)
        self._update_current_player()
        self._update_piece_type_board_state()

    def _validate_on_move(self, move: Move) -> None:
        """
        Validates a move.
        """
        if move.piece.color != self.current_player_color:
            raise ValueError("It is not the current player's turn.")

    def execute_update_validate_on_move(self, move: Move) -> None:
        """
        Executes a move.
        """
        self._validate_on_move(move)
        self.controller.initiate_move_and_related_methods(move)
        self._update_on_move(move)

    def get_game_status(self) -> GameStatus:
        """
        Returns the current status of the game (e.g., in-progress, checkmate, stalemate).
        """
        # TODO
        return GameStatus.ACTIVE

    def _update_piece_type_board_state(self) -> None:
        """
        This method creates and updates a board of piece types from the board of squares.
        New board structure for the API: list[list[(PieceType, Color) or None]]
        Program board structure: list[list[Square]]
        """
        board_of_squares = self.board_manager.board

        board_of_piece_types = [[(None, None) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                square = board_of_squares[row][col]
                if square.occupant:
                    board_of_piece_types[row][col] = square.occupant.piece_type, square.occupant.color
                else:
                    board_of_piece_types[row][col] = None, None

        self.piece_type_board_state = board_of_piece_types
