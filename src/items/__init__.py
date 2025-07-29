# src/items/__init__.py
from .registry import item_registry

def init_item_system():
    """初始化物品系统"""
    # 注册所有物品类型
    from .weapons.iron_hook import IronHook  # 延迟导入避免循环依赖
    item_registry.register_item_type("iron_hook", IronHook)
    from .weapons.firelock import Firelock
    item_registry.register_item_type("firelock", Firelock)