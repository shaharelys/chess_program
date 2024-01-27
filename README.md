# Chess Game Project

This project is a chess game framework in Python, created as a learning tool to explore and apply object-oriented programming (OOP) best practices, including clean code, SOLID principles, and various design patterns. It is not intended as a professional API but as an educational resource to demonstrate advanced programming concepts in a familiar game context.

## Current State of Development

This game is still under development, focusing on implementing and refining the core functionalities of chess gameplay within a structured OOP framework.


## Project Overview

- **game_manager.py**: Manages game state, including board setup and move history. It updates legal moves for pieces and integrates with `BoardManager` and `MoveFactory`.

- **board.py**: Manages the chessboard, handling board setup, piece placement, and occupancy checks. Includes `BoardManager` for board operations and `BoardSetup` for initial piece arrangement.

- **gui.py**: A simple GUI for testing purposes, built with tkinter. It displays the chessboard, updates board state, and handles user interactions for selecting and moving pieces.

- **move.py**: Contains the `Move` class representing chess moves, handling move validation and categorization (e.g., step, capture). Also includes `MoveValidation` and `MoveFactory` for move processing and creation.

- **config.py**: Defines constants and enums like `BOARD_SIZE`, `Color`, `PieceType`, and `MoveScope`, centralizing configuration settings for the game.

- **square.py**: Represents individual squares on the chessboard, tracking occupancy and control by chess pieces. Includes an `Operator` class for piece placement.

- **chess_piece.py**: Defines chess pieces (Pawn, Knight, Bishop, Rook, Queen, King) with their movements and control over squares. Uses abstract base class `ChessPiece` for shared functionality.

- **control_map.py**: Manages control maps and line-of-sight for pieces, updating controlled squares and handling piece movements.
