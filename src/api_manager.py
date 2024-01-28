# api_manager.py


class APIManager:
    def __init__(self, program_manager: 'ProgramManager'):
        """
        Initialize the API manager with a reference to the ProgramManager.
        """
        self._program_manager = program_manager

    def get_board_state(self) -> list[list[('PieceType', 'Color') or (None, None)]]:
        """
        Returns the current state of the chess board.
        """
        return self._program_manager.get_board_state()

    def get_legal_moves_positions(self, position: tuple[int, int]) -> set[tuple[int, int]]:
        """
        Returns a list of legal moves for the piece at the specified position.
        """
        return self._program_manager.get_legal_moves_positions(position)

    def execute_move_by_position(self, piece_current_position: tuple[int, int],
                                 piece_final_position: tuple[int, int]) -> None:
        """
        Executes a move on the board, given the current position of the piece and the wanted final position.
        """
        self._program_manager.execute_move_by_position(piece_current_position, piece_final_position)

    def get_game_status(self) -> 'GameStatus':
        """
        Returns the current status of the game (e.g., in-progress, checkmate, stalemate).
        """
        return self._program_manager.get_game_status()

    def get_current_player(self) -> 'Color':
        """
        Returns the current player's color.
        """
        return self._program_manager.get_current_player()