# square.py
from config import *
from typing import Optional


class Square:
    def __init__(self, position: tuple[int, int]):
        self.occupant: Optional['ChessPiece'] = None
        self.position = position
        self.color = self._get_square_color()
        self.controlled_by: set['ChessPiece'] = set()

    def _get_square_color(self) -> Color:
        """
        Returns the color of the board square.
        """
        row, col = self.position
        return Color.BLACK if (row + col) % 2 == 0 else Color.WHITE
