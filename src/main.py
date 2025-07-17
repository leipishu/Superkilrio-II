# src/main.py
import os
os.environ["PYGLET_AUDIO"] = "openal"

from src.game_controller import GameController
from src.welcome_screen import WelcomeScreen
from src.utils.logging_config import logger
import arcade
import atexit
import sys
import traceback

def silent_xaudio2_error(exctype, value, tb):
    # 只静默 XAudio2 的 OSError
    if exctype is OSError and (
        "XA2SourceVoice" in "".join(traceback.format_tb(tb)) or
        "xaudio2" in str(value).lower()
    ):
        return
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = silent_xaudio2_error


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

    def cleanup_on_exit():
        """退出时的清理函数"""
        try:
            if game_controller:
                game_controller.cleanup()
                logger.info("Game resources cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    # 注册退出时的清理函数
    atexit.register(cleanup_on_exit)

    welcome = WelcomeScreen(window, start_game, about, settings)
    window.show_view(welcome)

    try:
        arcade.run()
    finally:
        # 确保在arcade.run()结束后也进行清理
        cleanup_on_exit()

if __name__ == "__main__":
     main()