# board.py
from config import *
from chess_piece import *
from control_map import ControlMap
from typing import Callable


class BoardManager:
    def __init__(self, callback_initialize_piece: Callable[[ChessPiece, Square, 'BoardSetup'], None]):
        self.board: list[list[Square]] = BoardSetup(callback_initialize_piece).board
        self.threats_map = ControlMap()

    def get_square(self, row, col) -> Square:
        return self.board[row][col]

    def is_occupied(self, row, col):
        return self.get_square(row, col).occupant is not None


class BoardSetup:
    def __init__(self, callback_initialize_piece: Callable[[ChessPiece, Square, 'BoardSetup'], None]):
        self.callback_initialize_piece = callback_initialize_piece
        self.board: list[list[Square]] = self._create_blank_board()
        self._place_all_pieces()

    @staticmethod
    def _create_blank_board() -> list[list[Square]]:
        # Implement logic to create a blank board
        board = [[Square((i, j)) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
        return board

    def _place_single_piece(self, piece_type: PieceType, color: Color, position: tuple[int, int]):
        # Implement logic to place a single piece on the board
        square = self.board[position[0]][position[1]]  # a reference to the corresponding square
        piece = ChessPieceFactory.create(piece_type, color, square)
        self.callback_initialize_piece(piece, square, self)

    def _place_all_pieces(self):
        for init_piece in InitPiece:
            piece_type, color, positions = init_piece.value
            for pose in positions:
                self._place_single_piece(piece_type, color, pose)
