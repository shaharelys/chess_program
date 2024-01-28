# gui.py
import tkinter as tk
from api_manager import APIManager
from program_manager import ProgramManager
from config import BOARD_SIZE, Color, PieceType


class ChessGUI:
    def __init__(self, api_manager: APIManager):
        self.api_manager = api_manager
        self.root = tk.Tk()
        self.root.title("Chess Game")
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # 8x8 chess board
        self.create_graphic_board()
        self.selected_position = None
        self.cache_highlighted_squares: set[tuple[int, int]] = set()

    @property
    def board(self):
        """
        board: list[list[('PieceType', 'Color') or (None, None)]]
        """
        return self.api_manager.get_board_state()

    def create_graphic_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = "green" if (row + col) % 2 == 0 else "white"
                button = tk.Button(self.root, bg=color, command=lambda r=row, c=col: self.on_square_click(r, c))
                button.grid(row=row, column=col, sticky="nsew")
                self.buttons[row][col] = button
        self.update_graphic_board()

    def update_graphic_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece_type, piece_color = self.board[row][col]
                text = self.get_piece_symbol(piece_type, piece_color) if piece_type else ""
                self.buttons[row][col].config(text=text)
        self.root.update_idletasks()  # Update the GUI

    @staticmethod
    def get_piece_symbol(piece_type, piece_color):
        if piece_type is None:
            return ''
        type_str = piece_type.name[0]
        color_suffix = ' | W' if piece_color == Color.WHITE else ' | B'
        return type_str + color_suffix

    def run(self):
        for row in range(BOARD_SIZE):
            self.root.grid_rowconfigure(row, weight=1)
        for col in range(BOARD_SIZE):
            self.root.grid_columnconfigure(col, weight=1)
        self.root.mainloop()

    def on_square_click(self, row, col):
        void = (None, None)
        former_row, former_col = self.selected_position if self.selected_position else void
        former_selected_square_content = self.board[former_row][former_col] if self.selected_position else void
        new_square_content = self.board[row][col]

        # Reset the previously highlighted selected squares
        if self.cache_highlighted_squares:
            for move_row, move_col in self.cache_highlighted_squares:
                self.reset_square_highlight(move_row, move_col)

        # Handle user clicking on an empty square
        if former_selected_square_content == void and new_square_content == void:
            # Nothing to do here
            print("# state: IDLE")
            pass

        # Handle user selecting a piece
        elif former_selected_square_content == void and new_square_content != void:
            # User has clicked on a square with a piece, select this piece
            print("# State: SELECTED A PIECE")
            self.selected_position = (row, col)

            # Highlight the selected piece and its legal moves
            self.highlight_and_list_square(row, col)
            self.highlight_moves_of_piece_at_position(position=(row, col))

        # Handle user moving a selected piece
        elif former_selected_square_content != void and new_square_content == void:
            # Attempt to move the selected piece to the clicked empty square
            print("# State: STEP ATTEMPT")
            self.execute_move(self.selected_position, (row, col))
            self.selected_position = None

        # Handle user moving a selected piece to a square with another piece (capture scenario)
        elif former_selected_square_content != void and new_square_content != void:
            # Attempt to move the selected piece to capture the piece on the clicked square
            print("# State: CAPTURE ATTEMPT")
            self.execute_move(self.selected_position, (row, col))
            self.selected_position = None

        else:
            print("# State: Unidentified!")

    def execute_move(self, start_position, end_position):
        print(f"\t-> Attempting move")
        try:
            self.api_manager.execute_move_by_position(start_position, end_position)
            print("\t-> Attempt executed successfully.")
            self.update_graphic_board()  # Refresh the board
        except Exception as e:
            print(f"\t-> Error executing move: {e}")

    def highlight_and_list_square(self, row, col, color="yellow"):
        """
        Highlights the square at the specified row and column and lists it in cache.
        """
        print(f"\t-> Highlighting square at ({row}, {col})")
        self.buttons[row][col].config(bg=color)
        self.cache_highlighted_squares.add((row, col))

    def highlight_moves_of_piece_at_position(self, position):
        """
        Highlights the legal moves for the piece at the specified position.
        """
        row, col = position
        legal_moves = self.api_manager.get_legal_moves_positions((row, col))
        for move_row, move_col in legal_moves:
            self.highlight_and_list_square(move_row, move_col, color="light blue")

    def reset_square_highlight(self, row, col):
        color = "green" if (row + col) % 2 == 0 else "white"
        self.buttons[row][col].config(bg=color)


if __name__ == "__main__":
    program_manager = ProgramManager()
    api_manager = APIManager(program_manager)
    gui = ChessGUI(api_manager=api_manager)
    gui.run()
