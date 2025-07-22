# src/items/weapons/iron_hook.py
import os
from src.items.base_item import BaseItem
from src.constants import get_asset_path


class IronHook(BaseItem):
    def __init__(self):
        # JSON文件路径（与py文件同级）
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "iron_hook.json")

        super().__init__(json_path)

        # 调试日志
        print(f"JSON路径: {json_path}")
        print(f"贴图状态: {hasattr(self, 'texture')}")
        if hasattr(self, 'texture'):
            print(f"贴图尺寸: {self.texture.width}x{self.texture.height}")

    def use(self, player):
        """装备武器"""
        if hasattr(player, 'equip_weapon'):
            player.equip_weapon(self)
            return True
        return False