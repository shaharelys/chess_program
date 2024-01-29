# board.py
from config import *
from chess_piece import ChessPiece, ChessPieceFactory, King
from square import Square
from typing import Callable


class BoardManager:
    def __init__(self, callback_initialize_piece_on_board_setup: Callable[[ChessPiece, Square, 'BoardSetup'], None]):
        self.board_setup = BoardSetup(callback_initialize_piece_on_board_setup)
        self.board: list[list[Square]] = self.board_setup.board
        self.white_pieces_refs: set[ChessPiece] = self.board_setup.white_pieces_refs
        self.black_pieces_refs: set[ChessPiece] = self.board_setup.black_pieces_refs
        self.white_king_ref: King = next(piece for piece in self.white_pieces_refs if isinstance(piece, King))
        self.black_king_ref: King = next(piece for piece in self.black_pieces_refs if isinstance(piece, King))

    def get_square(self, row, col) -> Square:
        return self.board[row][col]

    def is_occupied(self, row, col):
        return self.get_square(row, col).occupant is not None


class BoardSetup:
    def __init__(self, callback_initialize_piece_on_board_setup: Callable[[ChessPiece, Square, 'BoardSetup'], None]):
        self.callback_initialize_piece_on_board_setup = callback_initialize_piece_on_board_setup
        self.board: list[list[Square]] = self._create_blank_board()
        self.chess_piece_factory = ChessPieceFactory()
        self.white_pieces_refs = set()
        self.black_pieces_refs = set()
        self._place_all_pieces()

    @staticmethod
    def _create_blank_board() -> list[list[Square]]:
        # Implement logic to create a blank board
        board = [[Square((i, j)) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
        return board

    def _add_piece_ref(self, piece: ChessPiece) -> None:
        if piece.color is Color.WHITE:
            self.white_pieces_refs.add(piece)
        else:
            self.black_pieces_refs.add(piece)

    def _place_single_piece(self, piece_type: PieceType, color: Color, position: tuple[int, int]):
        # Implement logic to place a single piece on the board
        piece = self.chess_piece_factory.create(piece_type, color)
        square = self.board[position[0]][position[1]]  # a reference to the corresponding square
        self._add_piece_ref(piece)
        self.callback_initialize_piece_on_board_setup(piece, square, self)

    def _place_all_pieces(self):
        for init_piece in InitPiece:
            piece_type, color, positions = init_piece.value
            for pose in positions:
                self._place_single_piece(piece_type, color, pose)
