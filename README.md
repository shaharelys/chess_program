# Chess Game Project

This project is a chess game framework in Python, created as a learning tool to explore and apply object-oriented programming (OOP) best practices, including clean code, SOLID principles, and various design patterns. It is not intended as a professional API but as an educational resource to demonstrate advanced programming concepts in a familiar game context.

## Current State of Development

This game is still under development, focusing on implementing and refining the core functionalities of chess gameplay within a structured OOP framework.

## Project Overview

- **gui.py**: Provides a basic graphical user interface for testing using tkinter, enabling user interactions with the game through visual elements via `ApiManager`.

- **api_manager.py**: Manages external API interactions, facilitating communication interface between the program and a client.

- **program_manager.py**: Serves as the main entry point for the application, initializing and coordinating various components of the game.

- **game_manager.py**: Handles the overarching game state, including turn management, move history, and game status updates.

- **game_controller.py**: Orchestrates game logic, handling move execution, pawn promotion, and check status. It integrates closely with `BoardManager` and `MoveFactory` to manage gameplay rules and piece interactions efficiently.

- **board_manager.py**: Responsible for managing the state and operations of the chessboard, including piece placements and board updates.

- **move.py**: Contains the `Move` class representing chess moves, handling move validation and categorization (e.g., step, capture). Also includes `MoveValidation` and `MoveFactory` for move processing and creation.

- **config.py**: Defines constants and enums like `BOARD_SIZE`, `Color`, `PieceType`, and `MoveScope`, centralizing configuration settings for the game.

- **square.py**: Defines the `Square` class representing a square on the chessboard, including its position, color, and piece.

- **chess_piece.py**: Defines chess pieces (Pawn, Knight, Bishop, Rook, Queen, King) with their movements and control over squares. Uses abstract base class `ChessPiece` for shared functionality.
