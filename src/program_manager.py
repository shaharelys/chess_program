# program_manager.py
from game_manager import GameManager
from config import PieceType, Color, GameStatus, BOARD_SIZE


class ProgramManager:
    def __init__(self):
        self._game_manager = GameManager()

    def get_board_state(self) -> list[list[(PieceType, Color) or (None, None)]]:
        """
        Returns the current state of the simplified chess board.
        """
        return self._game_manager.piece_type_board_state

    def get_legal_moves_positions_by_position(self, position: tuple[int, int]) -> set[tuple[int, int]]:
        """
        Returns a set of legal moves final positions for the piece at the specified position.
        """
        square = self._game_manager.board_manager.get_square(position[0], position[1])
        piece = square.occupant
        if not piece:
            assert piece is not None, "There is no piece on the specified square."
            return set()
        legal_moves = self._game_manager.controller.get_legal_moves(piece)
        legal_moves_final_positions = {move.square_final.position
                                       for move_scope_set in legal_moves.values()
                                       for move in move_scope_set if move.is_legal}
        return legal_moves_final_positions

    def execute_move_by_position(self, piece_current_position: tuple[int, int],
                                 piece_final_position: tuple[int, int]) -> None:
        """
        Executes a move on the board by the current position of the piece, and its wanted final position.
        """
        square_current = self._game_manager.board_manager.get_square(*piece_current_position)
        piece = square_current.occupant
        assert piece is not None, "There is no piece on the specified square."

        move = self._game_manager.controller.move_factory.create(piece, piece_final_position)
        if move and move.is_legal:
            self._game_manager.execute_update_validate_on_move(move)
        else:
            raise ValueError("Illegal move.")

    def get_game_status(self) -> GameStatus:
        return self._game_manager.get_game_status()

    def get_current_player(self) -> Color:
        return self._game_manager.current_player_color
