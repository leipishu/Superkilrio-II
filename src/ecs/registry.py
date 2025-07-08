from typing import Dict, Type, Any
import arcade

class EntityRegistry:
    """纯净的实体注册系统，无游戏具体内容"""
    def __init__(self):
        self._entity_types: Dict[str, Type] = {}
        self._active_entities = arcade.SpriteList()

    def register_blueprint(self, entity_type: str, entity_class: Type):
        """注册实体蓝图（无具体实现）"""
        self._entity_types[entity_type] = entity_class

    def create_entity(self, entity_type: str, **kwargs) -> arcade.Sprite:
        """创建实体实例"""
        cls = self._entity_types.get(entity_type)
        if not cls:
            raise ValueError(f"Unknown entity type: {entity_type}")
        return cls(**kwargs)

    def spawn(self, entity_type: str, x: float, y: float, **kwargs):
        """生成并管理实体"""
        entity = self.create_entity(entity_type, **kwargs)
        entity.center_x = x
        entity.center_y = y
        self._active_entities.append(entity)
        return entity

    def update_all(self, delta_time: float):
        """更新所有实体"""
        self._active_entities.update()
        self._active_entities.update_animation(delta_time)

    def draw_all(self):
        """绘制所有实体"""
        self._active_entities.draw()