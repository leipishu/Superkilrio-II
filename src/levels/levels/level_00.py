"""Level 00 implementation"""
from ..level_manager import Level as BaseLevel
from src.ecs.entities.npc.trainer import TrainerNPC
from src.constants import *
from src.utils.logging_config import logger
import arcade

LEVEL_NUM = 0

class Level(BaseLevel):
    """Level 00 concrete implementation"""
    def __init__(self):
        super().__init__()
        self.logger = logger.getChild(f"Level{LEVEL_NUM}")
        self.logger.debug("Level00 instance created")
        self.logger.debug(f"Parent class: {super().__class__.__name__}")
        self.logger.debug(f"Initial npcs list: {len(self.npcs)} items")

    def setup(self):
        self.logger.info("Starting level setup")
        try:
            # 创建教官NPC
            self.trainer = TrainerNPC()
            self.trainer.center_x = SCREEN_WIDTH // 2
            self.trainer.center_y = GROUND_Y + 100

            self.logger.debug(f"Creating NPC at position ({self.trainer.center_x}, {self.trainer.center_y})")
            self.logger.debug(f"NPCs list before append: {len(self.npcs)} items")

            self.npcs.append(self.trainer)

            self.logger.debug(f"NPCs list after append: {len(self.npcs)} items")
            self.logger.debug("NPC added successfully")

            # 本关可直接通过
            self.is_completed = True
            self.logger.info("Level setup completed")

        except Exception as e:
            self.logger.error(f"Level setup failed: {str(e)}")
            raise

    def draw(self):
        """绘制关卡内容"""
        try:
            super().draw()
            self.logger.debug("Level drawn successfully")
        except Exception as e:
            self.logger.error(f"Drawing failed: {str(e)}")
            raise