# gui.py
import tkinter as tk
from api_manager import APIManager
from program_manager import ProgramManager
from config import BOARD_SIZE, Color, PieceType, CheckStatus


class ChessGUI:
    def __init__(self, service: APIManager):
        self.api_manager = service
        self.root = tk.Tk()
        self.root.title("Chess Game")
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # 8x8 chess board
        self.create_graphic_board()
        self.piece_to_move_selected_position = None
        self.cache_highlighted_squares: set[tuple[int, int]] = set()

    """api methods:"""
    @property
    def check_status(self) -> CheckStatus:
        """
        Returns the current check status of the game
        """
        return self.api_manager.get_check_status()

    @property
    def board(self) -> list[list[(PieceType, Color) or (None, None)]]:
        """
        board: list[list[('PieceType', 'Color') or (None, None)]]
        """
        return self.api_manager.get_board_state()

    @property
    def current_player(self) -> Color:
        """
        Returns the current player's color of type 'Color'.
        """
        return self.api_manager.get_current_player()

    def get_legal_moves_positions_by_position(self, position: tuple[int, int]) -> set[tuple[int, int]]:
        return self.api_manager.get_legal_moves_positions_by_position(position)

    def execute_move(self, start_position: tuple[int, int], end_position: tuple[int, int]) -> None:
        print(f"\t-> Attempting move")
        try:
            self.api_manager.execute_move_by_position(start_position, end_position)
            print("\t-> Attempt executed successfully.")
            self.update_graphic_board()  # Refresh the board
        except Exception as e:
            print(f"\t-> Error executing move: {e}")

    """gui methods:"""

    def create_graphic_board(self) -> None:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = "green" if (row + col) % 2 == 0 else "white"
                button = tk.Button(self.root, bg=color, command=lambda r=row, c=col: self.on_square_click(r, c))
                button.grid(row=row, column=col, sticky="nsew")
                self.buttons[row][col] = button
        self.update_graphic_board()

    def update_graphic_board(self) -> None:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece_type, piece_color = self.board[row][col]
                text = self.get_piece_symbol(piece_type, piece_color) if piece_type else ""
                self.buttons[row][col].config(text=text)
        self.root.update_idletasks()  # Update the GUI

    @staticmethod
    def get_piece_symbol(piece_type: PieceType, piece_color: Color) -> str:
        """
        Returns the symbol of the piece.
        """
        if piece_type is None:
            return ''
        type_str = piece_type.name[0]
        color_suffix = '⬜' if piece_color == Color.WHITE else '⬛'
        return type_str + color_suffix

    def run(self) -> None:
        for row in range(BOARD_SIZE):
            self.root.grid_rowconfigure(row, weight=1)
        for col in range(BOARD_SIZE):
            self.root.grid_columnconfigure(col, weight=1)
        self.root.mainloop()

    def on_square_click(self, row, col) -> None:
        void = (None, None)
        prev_row, prev_col = self.piece_to_move_selected_position if self.piece_to_move_selected_position else void
        prev_selected_square_content = self.board[prev_row][prev_col] if self.piece_to_move_selected_position else void
        new_square_content = self.board[row][col]

        # Reset highlighted squares cache
        if self.cache_highlighted_squares:
            self.clean_cache_highlighted_squares()

        # 1. Handle user clicking on an empty square
        if prev_selected_square_content == void and new_square_content == void:
            print("# state: IDLE")
            pass

        # 2. Handle user selecting a piece
        elif prev_selected_square_content == void and new_square_content != void:
            print("# State: SELECTED A PIECE")
            self.piece_to_move_selected_position = (row, col)
            selected_piece_color = new_square_content[1]
            if selected_piece_color != self.current_player:
                print("\t-> Selected piece is not of the current player's color.")
                self.piece_to_move_selected_position = None
                return

            # Highlight the selected piece and its legal moves
            self.highlight_and_list_curr_piece_square(self.piece_to_move_selected_position)
            self.highlight_and_list_moves_of_piece_at_position(self.piece_to_move_selected_position)

        # 3. Handle user step attempt to a selected void square
        elif prev_selected_square_content != void and new_square_content == void:
            print("# State: STEP ATTEMPT")
            self.execute_move(self.piece_to_move_selected_position, (row, col))
            self.piece_to_move_selected_position = None

        # 4. Handle user capture attempt of a piece at a selected square
        elif prev_selected_square_content != void and new_square_content != void:
            print("# State: CAPTURE ATTEMPT")
            self.execute_move(self.piece_to_move_selected_position, (row, col))
            self.piece_to_move_selected_position = None

        else:
            raise ValueError("Unidentified state.")

    def highlight_and_list_square(self, position: tuple[int, int], color: str) -> None:
        """
        Highlights the square at the specified row and column and lists it in cache.
        """
        row, col = position
        print(f"\t-> Highlighting square at ({row}, {col})")
        self.buttons[row][col].config(bg=color)
        self.cache_highlighted_squares.add((row, col))

    def highlight_and_list_curr_piece_square(self, position: tuple[int, int]) -> None:
        """
        Highlights the square at the specified row and column and lists it in cache.
        """
        curr_piece_color = "yellow"
        self.highlight_and_list_square(position, curr_piece_color)

    def highlight_and_list_moves_of_piece_at_position(self, position: tuple[int, int]) -> None:
        """
        Highlights the legal moves for the piece at the specified position.
        """
        row, col = position
        legal_moves_color = "light blue"
        legal_moves = self.get_legal_moves_positions_by_position((row, col))
        for position in legal_moves:
            self.highlight_and_list_square(position, legal_moves_color)

    def clean_cache_highlighted_squares(self) -> None:
        """
        Resets the color of all squares in the cache.
        """
        for row, col in self.cache_highlighted_squares:
            self.reset_square_highlight(row, col)
        self.cache_highlighted_squares.clear()  # empties the cache

    def reset_square_highlight(self, row: int, col: int) -> None:
        color = "green" if (row + col) % 2 == 0 else "white"
        self.buttons[row][col].config(bg=color)


if __name__ == "__main__":
    program_manager = ProgramManager()
    api_manager = APIManager(program_manager)
    gui = ChessGUI(service=api_manager)
    gui.run()
