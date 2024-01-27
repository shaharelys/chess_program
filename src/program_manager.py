# program_manager.py
from game_manager import GameManager


class ProgramManager:
    def __init__(self):
        self.game_manager = GameManager()
        # Initialize other components like GUIManager, InputManager, etc.

    def start_game(self):
        # Method to start the game
        pass

    def handle_user_input(self, input_data):
        # Method to process user input
        pass

    def update_game_state(self):
        # Method to update the game state based on game logic
        pass

    def render(self):
        # Method to handle rendering of the game state (if GUI is separate)
        pass
