# src/main.py
from src.game_controller import GameController

def main():
    """游戏入口点"""
    game = GameController()
    game.run()

if __name__ == "__main__":
    main()