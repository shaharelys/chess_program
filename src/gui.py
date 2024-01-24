# gui.py
import tkinter as tk
from board_manager import BoardManager
from config import *


class ChessGUI:
    def __init__(self, root, board_manager: BoardManager):
        self.root = root
        self.board_manager = board_manager
        self.create_chess_board()
        self.update_board()  # Initial update to display the starting board

    def create_chess_board(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        self.labels = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                gui_row = BOARD_SIZE - 1 - i
                square = self.board_manager.get_square(i, j)
                bg_color = 'white' if square.color == Color.WHITE else 'green'
                label = tk.Label(self.board_frame, bg=bg_color, width=4, height=2)
                label.grid(row=gui_row, column=j)
                self.labels[i][j] = label

    def update_board(self):
        # Update the GUI to reflect the current state of the board
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                square = self.board_manager.get_square(i, j)
                piece = square.occupant
                text = self.get_piece_symbol(piece) if piece else ''
                self.labels[i][j].config(text=text)

    def get_piece_symbol(self, piece: 'ChessPiece'):
        # Return a textual representation of the chess piece
        # This method assumes that each type of ChessPiece has a unique symbol
        # You can modify this method to fit your ChessPiece class implementation
        if piece.piece_type == PieceType.PAWN:
            if piece.color == Color.WHITE:
                return '♙'
            else:
                return '♟'
        return piece.piece_type.symbol


# Running the GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess Game")

    game_board = BoardManager()
    app = ChessGUI(root, game_board)
    root.mainloop()
