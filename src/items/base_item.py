# src/items/base_item.py
import json
import os
from typing import Optional
import arcade
from src.constants import get_asset_path
from src.utils.logging_config import logger


class BaseItem:
    """物品基类(支持JSON配置)"""
    _json_cache = {}

    def __init__(self, json_file: str = None):
        if json_file:
            self.load_from_json(json_file)

    def load_from_json(self, json_file: str) -> bool:
        """从JSON文件加载物品配置"""
        try:
            if json_file not in self._json_cache:
                with open(json_file, 'r', encoding='utf-8') as f:
                    self._json_cache[json_file] = json.load(f)

            config = self._json_cache[json_file]
            self.item_id = config.get("item_id", "")
            self.name = config.get("name", "未命名物品")
            self.description = config.get("description", "")
            self.damage = config.get("damage", 10)
            self.attack_range = config.get("attack_range", 100)
            self.attack_speed = config.get("attack_speed", 1.0)
            self.scale = config.get("scale", 1.0)

            # 关键修改：贴图路径使用assets目录
            texture_path = config.get("texture", "")
            if texture_path:
                # 使用get_asset_path加载assets目录下的贴图
                self.texture = arcade.load_texture(get_asset_path(texture_path))
                print(f"贴图加载成功: {get_asset_path(texture_path)}")

            return True
        except Exception as e:
            logger.error(f"加载物品配置失败: {str(e)}")
            return False