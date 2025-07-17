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
from src.systems.combat_system import CombatSystem  # 新增导入
from src.systems.audio_manager import audio_manager  # 新增导入


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
        self.combat_system = CombatSystem(self)  # 新增战斗系统
        self.level_manager.game = self  # 建立反向引用

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

        # 主动热身音效，避免首次播放卡顿
        audio_manager.play_sound('hit', volume=0.0)
        audio_manager.play_sound('hurt', volume=0.0)

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
        self.combat_system.update(delta_time)
        self.combat_system.update(delta_time)

        if self.debug_mode and arcade.key.SPACE in self.held_keys:
            self.logger.debug(f"Player position: ({self.player.center_x:.1f}, {self.player.center_y:.1f})")

    def on_key_press(self, key, modifiers):
        self.input_handler.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.input_handler.on_key_release(key, modifiers)

    def cleanup(self):
        """彻底清理游戏资源，防止XAudio2误"""
        try:
            #1. 清理战斗系统的粒子系统（包含音频资源）
            if hasattr(self.combat_system, 'particle_system'):
                self.combat_system.particle_system.cleanup()
                logger.info("Combat system audio resources cleaned up")
            
            # 2. 清理全局音频管理器
            audio_manager.cleanup()
            logger.info("Global audio manager cleaned up")
            
            # 3. 强制垃圾回收
            import gc
            try:
                gc.collect()
                logger.debug("Game controller forced garbage collection completed")
            except Exception as gc_error:
                logger.warning(f"Game controller garbage collection failed: {gc_error}")
            
            logger.info("Game resources cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during game cleanup: {e}")

    def __del__(self):
        """确保资源被清理 - 备用方案"""
        try:
            self.cleanup()
        except:
            pass  # 在析构函数中忽略所有错误

    def run(self):
        self.setup()