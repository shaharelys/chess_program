# board.py
from config import *
from move import *
from square import Square
from chess_piece import *


class Board:
    def __init__(self):
        self.board = BoardSetup().board

    def get_square(self, row, col):
        return self.board[row][col]


class BoardSetup:
    def __init__(self):
        self.board = self.create_blank_board()
        self.place_pawns()      # adds pawns to the board
        self.place_knights()    # adds knights to the board
        self.place_bishops()    # adds bishops to the board
        self.place_rooks()      # adds rooks to the board
        self.place_queens()     # adds queens to the board
        self.place_kings()      # adds kings to the board

    @staticmethod
    def create_blank_board() -> list[list[Square]]:
        # Implement logic to create a blank board
        board = [[Square() for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        return board

    def place_single_piece(self, piece_type: PieceType, color: Color, position: tuple[int, int]):
        # Implement logic to place a single piece on the board
        square = self.board[position[0]][position[1]]  # a reference to the corresponding square
        piece = ChessPieceFactory.create(piece_type, color)
        square.set_piece(piece)

    def place_pawns(self):
        for i in range(BOARD_SIZE):
            self.place_single_piece(PieceType.PAWN, Color.WHITE, (1, i))
            self.place_single_piece(PieceType.PAWN, Color.BLACK, (6, i))

    def place_knights(self):
        self.place_single_piece(PieceType.KNIGHT, Color.WHITE, (0, 1))
        self.place_single_piece(PieceType.KNIGHT, Color.WHITE, (0, 6))
        self.place_single_piece(PieceType.KNIGHT, Color.BLACK, (7, 1))
        self.place_single_piece(PieceType.KNIGHT, Color.BLACK, (7, 6))

    def place_bishops(self):
        self.place_single_piece(PieceType.BISHOP, Color.WHITE, (0, 2))
        self.place_single_piece(PieceType.BISHOP, Color.WHITE, (0, 5))
        self.place_single_piece(PieceType.BISHOP, Color.BLACK, (7, 2))
        self.place_single_piece(PieceType.BISHOP, Color.BLACK, (7, 5))

    def place_rooks(self):
        self.place_single_piece(PieceType.ROOK, Color.WHITE, (0, 0))
        self.place_single_piece(PieceType.ROOK, Color.WHITE, (0, 7))
        self.place_single_piece(PieceType.ROOK, Color.BLACK, (7, 0))
        self.place_single_piece(PieceType.ROOK, Color.BLACK, (7, 7))

    def place_queens(self):
        self.place_single_piece(PieceType.QUEEN, Color.WHITE, (0, 3))
        self.place_single_piece(PieceType.QUEEN, Color.BLACK, (7, 3))

    def place_kings(self):
        self.place_single_piece(PieceType.KING, Color.WHITE, (0, 4))
        self.place_single_piece(PieceType.KING, Color.BLACK, (7, 4))
