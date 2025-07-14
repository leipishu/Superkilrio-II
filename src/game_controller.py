# src/game_controller.py
import arcade
from src.constants import *
from src.utils.logging_config import logger
from src.player import Player
from src.levels.level_manager import LevelManager
from src.ecs.systems.dialogue_system import DialogueSystem
from src.systems.physics_system import PhysicsSystem
from src.systems.interaction_system import InteractionSystem
from src.systems.input_handler import InputHandler
from src.systems.renderer import Renderer


class GameController(arcade.View):
    def __init__(self):
        super().__init__()
        self.logger = logger.getChild('GameController')

        # 初始化各子系统
        self.player = Player()
        self.level_manager = LevelManager()
        self.dialogue_system = DialogueSystem()
        self.physics_system = PhysicsSystem()
        self.interaction_system = InteractionSystem(self)
        self.input_handler = InputHandler(self)
        self.renderer = Renderer(self)
        self.level_manager.game = self  # 新增：建立反向引用

        # 其他属性
        self.background = None
        self.held_keys = set()
        self.debug_mode = True
        self.font_name = "Microsoft YaHei"

    def setup(self):
        """初始化游戏资源"""
        try:
            self.background = arcade.load_texture(get_asset_path("background.png"))
            self.logger.info("Background loaded successfully")
        except Exception as e:
            self.logger.error(f"Background loading failed: {str(e)}")

        self.level_manager.load_levels()
        self.level_manager.goto_level(0, player=self.player)

    def on_draw(self):
        self.renderer.draw()

    def on_update(self, delta_time):
        self.player.update()
        self.player.update_animation(delta_time)
        self.level_manager.update(delta_time)
        self.interaction_system.check_npc_proximity()
        self.physics_system.apply_physics(self.player)
        if self.debug_mode and arcade.key.SPACE in self.held_keys:
            self.logger.debug(f"Player position: ({self.player.center_x:.1f}, {self.player.center_y:.1f})")

    def on_key_press(self, key, modifiers):
        self.input_handler.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.input_handler.on_key_release(key, modifiers)

    def run(self):
        self.setup()