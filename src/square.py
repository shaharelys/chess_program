# square.py
from __future__ import annotations
from config import *
from typing import Optional


class Square:
    def __init__(self, position: tuple[int, int]):
        self.occupant: Optional['ChessPiece'] = None
        self.position = position
        self.color = self.get_square_color()
        self.controlled_by: set['ChessPiece'] = set()
        self.operator = Operator(self)

    def get_square_color(self) -> Color:
        """
        Returns the color of the board square.
        """
        row, col = self.position
        return Color.BLACK if (row + col) % 2 == 0 else Color.WHITE


class Operator:
    def __init__(self, square: Square):
        self.square = square

    def set_piece(self, piece: 'ChessPiece'):
        """
        Place a piece on this square.
        """
        self.square.occupant = piece

    def remove_piece(self):
        """
        Remove any piece occupying this square.
        """
        self.square.occupant = None
