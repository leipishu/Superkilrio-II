# src/items/weapons/firelock.py
import os
from src.items.base_item import BaseItem
from src.constants import get_asset_path
from src.utils.logging_config import logger


class Firelock(BaseItem):
    def __init__(self):
        # JSON文件路径（与py文件同级）
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "firelock.json")

        logger.debug("=== Firelock Start Initializing ===")
        logger.debug(f"Trying to load JSON file from: {json_path}")

        super().__init__(json_path)

        # 调试日志
        logger.debug(f"JSON file loaded: {json_path}")
        logger.debug(f"Texture exisits: {hasattr(self, 'texture')}")
        if hasattr(self, 'texture'):
            logger.debug(f"Texture size: {self.texture.width}x{self.texture.height}")
        else:
            logger.warning("Texture not found")

        logger.debug("=== Firelock Initialized ===")

    def use(self, player):
        """装备/取消装备武器"""
        logger.debug(f"Attempting to toggle weapon {self.name}")

        # 如果已经装备了这个武器，则取消装备
        if hasattr(player,
                   'equipped_weapon') and player.equipped_weapon and player.equipped_weapon.item_id == self.item_id:
            player.unequip_weapon()
            logger.info(f"Weapon {self.name} Unequipped")
            return True

        # 否则装备武器
        if hasattr(player, 'equip_weapon'):
            player.equip_weapon(self)
            logger.info(f"Weapon {self.name} Equipped")
            return True

        logger.warning("The player does not have equip_weapon method")
        return False