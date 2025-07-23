# src/items/weapons/iron_hook.py
import os
from src.items.base_item import BaseItem
from src.constants import get_asset_path
from src.utils.logging_config import logger


class IronHook(BaseItem):
    def __init__(self):
        # JSON文件路径（与py文件同级）
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "iron_hook.json")

        logger.debug("=== IronHook初始化开始 ===")
        logger.debug(f"尝试从JSON文件加载配置: {json_path}")

        super().__init__(json_path)

        # 调试日志
        logger.debug(f"JSON配置加载完成，路径: {json_path}")
        logger.debug(f"贴图属性存在: {hasattr(self, 'texture')}")
        if hasattr(self, 'texture'):
            logger.debug(f"贴图尺寸: {self.texture.width}x{self.texture.height}")
        else:
            logger.warning("物品贴图未加载成功")

        logger.debug("=== IronHook初始化完成 ===")

    def use(self, player):
        """装备武器"""
        logger.debug(f"尝试装备武器给玩家: {self.name}")
        if hasattr(player, 'equip_weapon'):
            player.equip_weapon(self)
            logger.info(f"武器 {self.name} 装备成功")
            return True
        logger.warning("玩家对象没有equip_weapon方法")
        return False