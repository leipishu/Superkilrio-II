import arcade
import importlib
from pathlib import Path
from typing import Dict, Type
from src.constants import *
from src.utils.logging_config import logger


class Level:
    """Base class for level"""

    def __init__(self):
        self.enemies = arcade.SpriteList()
        self.npcs = arcade.SpriteList()
        self.is_completed = False

    def setup(self):
        """Initialize level content"""
        pass

    def update(self, delta_time: float):
        """Update level logic"""
        # Change point 2: Add NPC physics update
        for npc in self.npcs:
            npc.change_y -= GRAVITY
            if npc.bottom <= GROUND_Y:
                npc.bottom = GROUND_Y
                npc.change_y = 0

        for enemy in self.enemies:
            enemy.change_y -= GRAVITY  # 应用重力
            enemy.center_y += enemy.change_y  # 更新位置

            # 地面检测
            if enemy.bottom <= GROUND_Y:
                enemy.bottom = GROUND_Y
                enemy.change_y = 0

        if len(self.enemies) == 0:
            self.is_completed = True

    def draw(self):
        """Draw level content"""
        self.enemies.draw()
        self.npcs.draw()


class LevelManager:
    def __init__(self):
        self.logger = logger.getChild('LevelManager')
        self.levels: Dict[int, Type[Level]] = {}
        self.current_level: Level = None
        self.current_level_num = -1

    def register_level(self, level_num: int, level_class: Type[Level]):
        """Register level class"""
        self.levels[level_num] = level_class

    def load_levels(self):
        """Automatically load all levels"""
        levels_dir = Path(__file__).parent.parent / "levels" / "levels"
        self.logger.info(f"Scanning levels directory: {levels_dir}")

        for py_file in levels_dir.glob("level_*.py"):
            self.logger.info(f"Level file found: {py_file.name}")
            module_name = f"levels.levels.{py_file.stem}"

            try:
                module = importlib.import_module(module_name)
                self.logger.info(f"Module imported successfully: {module_name}")

                if hasattr(module, "LEVEL_NUM"):
                    self.logger.info(f"Level number: {module.LEVEL_NUM}")
                else:
                    self.logger.warning("Module missing LEVEL_NUM constant")

                if hasattr(module, "Level"):
                    level_class = module.Level
                    self.logger.debug(f"Level class found: {level_class.__name__}")
                    self.logger.debug(f"Base class: {level_class.__bases__}")

                    if level_class.__bases__[0].__name__ == "Level":
                        self.register_level(module.LEVEL_NUM, level_class)
                        self.logger.info(f"Level registered: {module.LEVEL_NUM}")
                    else:
                        self.logger.warning(f"Ignoring non-standard level class: {level_class.__name__}")
                else:
                    self.logger.warning("Module missing Level class")

            except Exception as e:
                self.logger.error(f"Failed to load module: {module_name} - {str(e)}")

    def goto_level(self, level_num: int):
        """Go to specified level"""
        self.logger.info(f"Attempting to load level {level_num}")
        if level_num not in self.levels:
            raise ValueError(f"Level {level_num} not found")

        self.logger.info(f"Level class found: {self.levels[level_num].__name__}")

        # Debugging level instantiation process
        self.logger.debug("Starting to instantiate level...")
        level_class = self.levels[level_num]
        self.current_level = level_class()
        self.logger.debug(f"Level instantiation completed: {self.current_level}")

        # Check instance attributes
        self.logger.debug(f"Instance attribute check - npcs: {hasattr(self.current_level, 'npcs')}")
        self.logger.debug(f"Base class initialization status: {'Level' in [base.__name__ for base in level_class.__bases__]}")

        self.logger.debug("Calling level setup() method")
        self.current_level.setup()

        # In-depth debugging NPC list
        if hasattr(self.current_level, 'npcs'):
            self.logger.debug(f"Current level NPC count: {len(self.current_level.npcs)}")
            self.logger.debug(f"npcs list type: {type(self.current_level.npcs)}")
            if len(self.current_level.npcs) > 0:
                for i, npc in enumerate(self.current_level.npcs):
                    self.logger.debug(f"   NPC{i}: Type({type(npc)}), Position({npc.center_x}, {npc.center_y}), Size({npc.width}x{npc.height})")
            else:
                self.logger.warning("npcs list is empty")

        self.current_level_num = level_num
        self.logger.info(f"Level loaded successfully: {level_num}")

    def next_level(self):
        """Go to next level"""
        self.goto_level(self.current_level_num + 1)

    def update(self, delta_time: float):
        """Update current level"""
        if self.current_level:
            self.current_level.update(delta_time)

    def draw(self):
        """Draw current level"""
        if self.current_level:
            self.current_level.draw()
