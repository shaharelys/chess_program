# game_manager.py
"""
Manages a single game logic, including move processing, game state maintenance, and enforcing rules.
"""
from config import *
from board_manager import BoardManager, BoardSetup
from game_controller import GameController
from square import Square
from chess_piece import ChessPiece
from move import Move


class GameManager:
    def __init__(self):
        self.board_manager = BoardManager(GameController._initialize_piece)  # TODO: solve issue related to this method
        self.controller = GameController(self.board_manager)
        self.history: list[Move] = []
        self.current_player = Color.WHITE

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

    def execute_move(self, move: Move) -> None:
        """
        Executes a move.
        """
        self.controller.initiate_move_and_related_methods(move)
        self._update_on_move(move)
