# game_manager.py
"""
Manages a single game logic, including move processing, game state maintenance, and enforcing rules.
"""
from config import *
from board_manager import BoardManager
from game_controller import GameController
from move import Move


class GameManager:
    def __init__(self):
        self.controller = GameController()
        self.board_manager = self.controller.board_manager
        self.history: list[Move] = []
        self.current_player = Color.WHITE
        self.piece_type_board_state = None
        self._update_piece_type_board_state()

    def _update_history(self, move: Move) -> None:
        """
        Updates the history of moves.
        """
        self.history.append(move)

    def _update_current_player(self) -> None:
        """
        Updates the current player.
        """
        self.current_player = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK

    def _update_on_move(self, move: Move) -> None:
        """
        Updates the game state after a move has been made.
        """
        self._update_history(move)
        self._update_current_player()
        self._update_piece_type_board_state()

    def execute_move(self, move: Move) -> None:
        """
        Executes a move.
        """
        self.controller.initiate_move_and_related_methods(move)
        self._update_on_move(move)

    def get_game_status(self) -> GameStatus:
        """
        Returns the current status of the game (e.g., in-progress, checkmate, stalemate).
        """
        # TODO
        return GameStatus.ACTIVE

    def _update_piece_type_board_state(self) -> list[list[(PieceType, Color) or (None, None)]]:
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
