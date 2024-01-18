# square.py
from config import *
from chess_piece import ChessPiece


class Square:
    def __init__(self):
        self.occupied_by = None  # This can hold a reference to the piece occupying the square, if any
        self.threatened_by_white = set()  # Set of pieces (references) threatening this square
        self.threatened_by_black = set()  # Similarly, for black pieces

    def set_piece(self, material: ChessPiece):
        """
        Place a piece on this square.
        """
        self.occupied_by = material

    def remove_piece(self):
        """
        Remove any piece occupying this square.
        """
        self.occupied_by = None

    def add_threat(self, piece):
        """
        Add a piece to the set of pieces threatening this square.
        """
        if piece.color == Color.WHITE:
            self.threatened_by_white.add(piece)
        else:
            self.threatened_by_black.add(piece)

    def remove_threat(self, piece):
        """
        Remove a piece from the set of pieces threatening this square.
        """
        if piece.color == Color.WHITE:
            self.threatened_by_white.discard(piece)
        else:
            self.threatened_by_black.discard(piece)

    def is_under_threat(self, color: Color) -> bool:
        """
        Check if the square is under threat from the specified color.
        """
        if color == Color.WHITE:
            return len(self.threatened_by_white) > 0
        else:
            return len(self.threatened_by_black) > 0
