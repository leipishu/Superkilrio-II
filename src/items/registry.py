# src/items/registry.py
from typing import Dict, Type, Optional
import importlib
from pathlib import Path
from src.items.base_item import BaseItem
from src.utils.logging_config import logger


class ItemRegistry:
    """物品注册与管理中心"""

    def __init__(self):
        self._item_classes: Dict[str, Type[BaseItem]] = {}
        self._loaded_items: Dict[str, BaseItem] = {}

    def register_item(self, item_class: Type[BaseItem]):
        """注册物品类"""
        if not hasattr(item_class, 'item_id'):
            raise ValueError("物品类必须定义item_id属性")
        self._item_classes[item_class.item_id] = item_class

    def load_item_modules(self):
        """自动加载items目录下的所有物品模块"""
        items_dir = Path(__file__).parent
        for item_type in ["weapons", "quest_items"]:
            for py_file in (items_dir / item_type).glob("*.py"):
                if py_file.name.startswith("_"):
                    continue

                module_name = f"src.items.{item_type}.{py_file.stem}"
                try:
                    module = importlib.import_module(module_name)
                    for attr in dir(module):
                        cls = getattr(module, attr)
                        if (isinstance(cls, type) and
                                issubclass(cls, BaseItem) and
                                cls != BaseItem):
                            self.register_item(cls)
                except Exception as e:
                    logger.error(f"加载物品模块失败: {module_name} - {str(e)}")

    def create_item(self, item_id: str, **kwargs) -> Optional[BaseItem]:
        """创建物品实例"""
        if item_id not in self._item_classes:
            logger.error(f"未知物品ID: {item_id}")
            return None

        try:
            item = self._item_classes[item_id](**kwargs)
            if not item.load_texture(self._get_texture_path(item)):
                return None
            return item
        except Exception as e:
            logger.error(f"创建物品失败: {item_id} - {str(e)}")
            return None

    def _get_texture_path(self, item: BaseItem) -> str:
        """获取物品贴图路径"""
        item_type = "weapons" if "weapon" in item.item_id else "quest_items"
        return f"items/{item_type}/{item.item_id}.png"

    def preload_items(self, item_ids: list):
        """预加载常用物品"""
        for item_id in item_ids:
            if item_id not in self._loaded_items:
                item = self.create_item(item_id)
                if item:
                    self._loaded_items[item_id] = item

    def get_item(self, item_id: str) -> Optional[BaseItem]:
        """获取已加载的物品实例"""
        return self._loaded_items.get(item_id)