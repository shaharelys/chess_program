# game_manager.py
"""
Manages a single game logic, including move processing, game state maintenance, and enforcing rules.
"""
from config import *
from game_controller import GameController
from move import Move
from chess_piece import ChessPiece, King
from copy import deepcopy


class GameManager:
    def __init__(self):
        self.controller = GameController()
        self.board_manager = self.controller.board_manager
        self.history: list[tuple[Move, HistoryTag]] = []
        self.current_player_color = Color.WHITE
        self.piece_type_board_state = None
        self._update_piece_type_board_state()
        self.check_status: CheckStatus = CheckStatus.NO_CHECK
        self.white_king: King = self.board_manager.white_king
        self.black_king: King = self.board_manager.black_king

    def _update_check_status(self, move: Move) -> None:
        """
        Updates the check status of the game.
        """
        self.check_status = self.controller.get_check_status(move)

    def _update_history(self, move: Move, tag: HistoryTag) -> None:
        """
        Updates the history of moves.
        """
        self.history.append((move, tag))

    def _update_current_player(self) -> None:
        """
        Updates the current player.
        """
        self.current_player_color = Color.WHITE if self.current_player_color == Color.BLACK else Color.BLACK

    def _update_on_move(self, move: Move, history_tag: HistoryTag) -> None:
        """
        Updates the game state after a move has been made.
        """
        self._update_history(move, history_tag)
        self._update_current_player()
        self._update_piece_type_board_state()
        self._update_check_status(move)

    def _validate_on_move(self, move: Move) -> None:
        """
        Validates a move.
        """
        if move.piece.color != self.current_player_color:
            raise ValueError("It is not the current player's turn.")

        if self.check_status is not CheckStatus.NO_CHECK and not self._is_unchecking_king(move):
            raise ValueError("The current player is under check and must uncheck their king.")

    def _is_unchecking_king(self, move: Move) -> bool:
        """
        Returns True if the specified move unchecks the king.
        This method is computationally expensive, and should be used only when the current player is under check.
        """
        # get a deep copy of the game controller and the move
        controller_copy = deepcopy(self.controller)

        # create a same move copy for the copy (It must hold references of the new environment objects)
        piece_position = move.piece.square.position
        move_final_position: tuple[int, int] = move.square_final.position
        piece_copy = controller_copy.board_manager.get_square(*piece_position).occupant

        move_copy = controller_copy.move_factory.create(piece=piece_copy, position_final=move_final_position)

        # initiate the move copy in the copy
        controller_copy.initiate_move_and_related_methods(move_copy)

        # check if any of the opponent pieces is threatening the king in the copy
        my_color = move_copy.piece.color
        my_king_copy = controller_copy.white_king if my_color is Color.WHITE else controller_copy.black_king
        opponent_pieces_copy = controller_copy.board_manager.white_pieces if my_color is Color.BLACK \
            else controller_copy.board_manager.black_pieces

        for piece in opponent_pieces_copy:
            if my_king_copy.square in controller_copy.get_threatened_squares(piece):
                return False

        return True

    def execute_update_validate_on_move(self, move: Move) -> None:
        """
        Executes a move.
        """
        self._validate_on_move(move)
        history_tag = self.controller.initiate_move_and_related_methods(move)
        self._update_on_move(move, history_tag)

    def get_game_status(self) -> GameStatus:
        """
        Returns the current status of the game (e.g., in-progress, checkmate, stalemate).
        """
        # TODO
        return GameStatus.ACTIVE

    def _update_piece_type_board_state(self) -> None:
        """
        This method creates and updates a board of piece types from the board of squares.
        New board structure for the API: list[list[(PieceType, Color) or None]]
        Program board structure: list[list[Square]]
        """
        board_of_squares = self.board_manager.board

        board_of_piece_types = [[(None, None) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                square = board_of_squares[row][col]
                if square.occupant:
                    board_of_piece_types[row][col] = square.occupant.piece_type, square.occupant.color
                else:
                    board_of_piece_types[row][col] = None, None

        self.piece_type_board_state = board_of_piece_types
