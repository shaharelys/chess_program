# board.py
from config import *
from move import *
from square import Square
from chess_piece import *
from control_map import ControlMap


class BoardManager:
    def __init__(self):
        self.board: list[list[Square]] = BoardSetup().board
        self.threats_map = ControlMap()

    def get_square(self, row, col):
        return self.board[row][col]


class BoardSetup:
    def __init__(self):
        self.board: list[list[Square]] = self.create_blank_board()
        self.place_all_pieces()

    @staticmethod
    def create_blank_board() -> list[list[Square]]:
        # Implement logic to create a blank board
        board = [[Square((i, j)) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
        return board

    def place_single_piece(self, piece_type: PieceType, color: Color, position: tuple[int, int]):
        # Implement logic to place a single piece on the board
        square = self.board[position[0]][position[1]]  # a reference to the corresponding square
        piece = ChessPieceFactory.create(piece_type, color, square)
        square.operator.set_piece(piece)

    def place_all_pieces(self):
        for init_piece in InitPiece:
            piece_type, color, positions = init_piece.value
            for pose in positions:
                self.place_single_piece(piece_type, color, pose)
