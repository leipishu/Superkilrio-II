# src/items/base_item.py
import arcade
from typing import Optional
from src.constants import get_asset_path
from src.utils.logging_config import logger


class BaseItem:
    """物品基类"""

    def __init__(self):
        self.item_id = ""  # 物品唯一ID
        self.name = "未命名物品"  # 物品名称
        self.description = ""  # 物品描述
        self.texture = None  # 物品贴图
        self.scale = 1.0  # 显示缩放比例
        self.is_stackable = False  # 是否可堆叠
        self.max_stack = 1  # 最大堆叠数

    def load_texture(self, texture_path: str) -> bool:
        """加载物品贴图"""
        try:
            self.texture = arcade.load_texture(get_asset_path(texture_path))
            return True
        except Exception as e:
            logger.error(f"加载物品贴图失败: {texture_path} - {str(e)}")
            return False

    def use(self, player) -> bool:
        """使用物品的抽象方法"""
        raise NotImplementedError("必须实现use方法")

    def get_sprite(self, x: float, y: float) -> Optional[arcade.Sprite]:
        """获取物品精灵实例"""
        if not self.texture:
            return None

        sprite = arcade.Sprite()
        sprite.texture = self.texture
        sprite.scale = self.scale
        sprite.center_x = x
        sprite.center_y = y
        sprite.item_data = self  # 将物品数据附加到精灵上
        return sprite