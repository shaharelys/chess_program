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
        self.move_factory = MoveFactory(self)

    def get_square(self, row, col):
        return self.board[row][col]

    def is_occupied(self, row, col):
        return self.get_square(row, col).occupant is not None

    @staticmethod
    def update_controlled_squares(piece: ChessPiece) -> None:
        """
        Updates the set of squares controlled by this piece.
        """
        pass

    def update_legal_moves(self, piece: ChessPiece) -> None:
        """
        Updates the set of legal moves for this piece.
        """
        piece.legal_moves.clear()  # Clear current legal moves
        hypothetical_moves_final_positions = piece.get_hypothetical_moves_final_positions()

        for pose in hypothetical_moves_final_positions:
            square_final = self.get_square(*pose)
            move = self.move_factory.get_move(piece, square_final)

            if move.scope in {MoveScope.STEP, MoveScope.CAPTURE}:
                piece.legal_moves.add(move)


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
