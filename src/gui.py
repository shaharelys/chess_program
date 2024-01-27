# gui.py
import tkinter as tk
from board_manager import BoardManager
from config import *
from chess_piece import ChessPiece


class ChessGUI:
    def __init__(self, root, board_manager: BoardManager):
        self.root = root
        self.board_manager = board_manager
        self.create_chess_board()
        self.update_board()  # Initial update to display the starting board
        self.selected_piece = None

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
                # Use default arguments to capture the current values of i and j
                label.bind("<Button-1>", lambda e, row=i, col=j: self.on_square_click(row, col))

    def update_board(self):
        # Update the GUI to reflect the current state of the board
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                square = self.board_manager.get_square(i, j)
                piece = square.occupant
                text = self.get_piece_symbol(piece) if piece else ''
                self.labels[i][j].config(text=text)

    @staticmethod
    def get_piece_symbol(piece: ChessPiece):
        """
        Returns the symbol of the chess piece.
        """
        if piece.piece_type == PieceType.PAWN:
            if piece.color == Color.WHITE:
                return '♙'
            else:
                return '♟'
        return piece.piece_type.symbol

    def highlight_move(self, piece: ChessPiece):
        def _highlight_piece_move_options():
            squares_to_highlight = list(piece.controlled_squares)
            for square in squares_to_highlight:
                self.highlight_square(square.position, 'light blue')

        def _highlight_piece():
            self.highlight_square(piece.square.position, 'blue')

        _highlight_piece_move_options()
        _highlight_piece()

    def highlight_square(self, pose: tuple[int, int], color: str):
        i, j = pose
        self.labels[i][j].config(bg=color)

    def try_move_piece(self, row, col):
        """
        Logic to move the selected piece to the target square
        This includes updating the board state and the GUI
        Reset the selected piece after moving
        """
        self.selected_piece = None
        self.update_board()  # Refresh the board display

    def on_square_click(self, row, col):
        square = self.board_manager.get_square(row, col)
        if self.selected_piece:
            # Get the legal move positions for the selected piece
            legal_moves_positions = self.get_legal_moves_positions(self.selected_piece)

            if (row, col) in legal_moves_positions:
                # Attempt to move the selected piece to the clicked square
                self.try_move_piece(row, col)
            else:
                # Clicked outside of legal moves, deselect and clear highlights
                self.clear_highlights()
                if square.occupant != self.selected_piece:
                    # If clicked on a different piece, select the new piece
                    self.selected_piece = square.occupant
                    self.board_manager.update_legal_moves(square.occupant)  # TODO: fix this after GameManager intro
                    self.highlight_move(square.occupant)
                else:
                    # If clicked on a non-occupied square or the same piece, release the current selection
                    self.selected_piece = None
        elif square.occupant:
            # Select the new piece and highlight its legal moves
            self.selected_piece = square.occupant
            self.board_manager.update_legal_moves(square.occupant)
            self.highlight_move(square.occupant)

    def clear_highlights(self):
        # Clear all previous highlights
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                square = self.board_manager.get_square(i, j)
                bg_color = 'white' if square.color == Color.WHITE else 'green'
                self.labels[i][j].config(bg=bg_color)

        # If needed, also clear any text or other configurations related to highlights
        # ...

    def try_move_piece(self, row, col):
        # Logic to move the piece, which should also include clearing the highlights
        self.clear_highlights()
        # ... rest of the movement logic ...
        self.selected_piece = None
        self.update_board()  # Refresh the board display

    def get_legal_moves_positions(self, piece: ChessPiece):
        """
        Returns a list of tuples representing the positions of all legal moves for the piece.
        """
        legal_moves = []
        for move_set in piece.legal_moves.values():
            legal_moves.extend([move.square_final for move in move_set])
        return legal_moves


    def test_1(self, test_row: int, test_col: int):
        piece = self.board_manager.get_square(test_row, test_col).occupant
        self.board_manager.update_legal_moves(piece)
        self.highlight_move(piece)


# Running the GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess Game")

    game_board = BoardManager()
    app = ChessGUI(root, game_board)

    root.mainloop()