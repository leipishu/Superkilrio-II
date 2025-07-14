# src/main.py
from src.game_controller import GameController
from src.welcome_screen import WelcomeScreen
import arcade

def main():
    """游戏入口点"""
    window = arcade.Window(1440, 1080, "Superkilrio")
    game_controller = None
    welcome = None

    def start_game():
        nonlocal game_controller
        game_controller = GameController()
        arcade.set_viewport(0, 1440, 0, 1080)
        window.show_view(game_controller)
        game_controller.setup()

    def about():
        nonlocal welcome
        if welcome:
            welcome.show_about()

    def settings():
        # Simple settings popup for now
        arcade.close_window()
        print("Settings: (not implemented)")

    welcome = WelcomeScreen(window, start_game, about, settings)
    window.show_view(welcome)
    arcade.run()

if __name__ == "__main__":
    main()