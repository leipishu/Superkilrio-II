# src/items/registry.py
from typing import Dict, Optional
from src.items.base_item import BaseItem
from src.utils.logging_config import logger


class ItemRegistry:
    """物品注册与管理中心"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        self.logger = logger.getChild('ItemRegistry')
        if self._initialized:
            return
        self._item_classes: Dict[str, type[BaseItem]] = {}
        self._loaded_items: Dict[str, BaseItem] = {}
        self._initialized = True

    def register_item_type(self, item_id: str, item_class: type[BaseItem]):
        """注册物品类型"""
        if not issubclass(item_class, BaseItem):
            raise ValueError("The item class must be subclass of BaseItem.")
        self._item_classes[item_id] = item_class
        self.logger.info(f"Registered {item_id}")

    def create_item(self, item_id: str) -> Optional[BaseItem]:
        """创建物品实例"""
        if item_id not in self._item_classes:
            self.logger.error(f"Unknown item id: {item_id}")
            return None

        try:
            item = self._item_classes[item_id]()
            if not hasattr(item, 'texture') or item.texture is None:
                self.logger.warning(f"Item {item_id} has no texture")
            return item
        except Exception as e:
            self.logger.error(f"Failed to create {item_id} - {str(e)}")
            return None


# 全局单例实例
item_registry = ItemRegistry()