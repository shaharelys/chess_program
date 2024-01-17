# material.py

from abc import ABC, abstractmethod
from config import *


class Material(ABC):
    """
    Abstract class representing a chess piece.
    """

    def __init__(self, color: str, position: tuple[int, int]) -> None:
        self.color = color
        self.position = position

    @abstractmethod
    def potential_moves(self) -> list[tuple[int, int]]:
        """
        Generate all potential moves (both steps and captures) for the piece
        regardless of the current game state.
        """
        pass

    def filter_out_of_bounds_moves(self, moves: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Filter out moves that are out of the boundaries of the chessboard.
        """
        return [move for move in moves if self.is_within_bounds(move)]

    @staticmethod
    def is_within_bounds(position: tuple[int, int]) -> bool:
        """
        Check if a position is within the 8x8 chessboard.
        """
        row, col = position
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def valid_steps(self, board) -> list[tuple[int, int]]:
        """
        Filter potential moves to return only valid steps (non-capturing moves)
        considering the current game state.
        """
        # Implement logic to determine valid steps
        pass

    def valid_captures(self, board) -> list[tuple[int, int]]:
        """
        Filter potential moves to return only valid captures (capturing moves)
        considering the current game state.
        """
        # Implement logic to determine valid captures
        pass

# Subclasses like Pawn, Knight, etc., would implement the potential_moves method
