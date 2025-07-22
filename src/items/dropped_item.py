# src/ecs/entities/items/dropped_item.py
import arcade
from src.constants import *


class DroppedItem(arcade.Sprite):
    """具有物理效果的掉落物实体"""

    def __init__(self, item, x: float, y: float):
        super().__init__()

        # 基础属性
        self.item_data = item  # 关联的物品数据
        self.texture = item.texture
        self.scale = item.scale
        self.center_x = x
        self.center_y = y

        # 物理参数
        self.change_y = 3.0  # 初始弹跳速度
        self.gravity = 0.5  # 重力加速度
        self.friction = 0.9  # 地面摩擦力

        # 精确碰撞箱（基于贴图）
        self.set_hit_box(self.texture.hit_box_points)

        # 状态标记
        self.is_on_ground = False
        self.bounces = 0
        self.max_bounces = 2  # 最大弹跳次数

    def update(self):
        """物理更新"""
        # 应用重力
        if not self.is_on_ground:
            self.change_y -= self.gravity
            self.center_y += self.change_y

        # 地面检测
        if self.bottom <= GROUND_Y and self.change_y < 0:
            self.bottom = GROUND_Y
            self.change_y = -self.change_y * 0.6  # 弹性衰减
            self.bounces += 1

            if self.bounces >= self.max_bounces:
                self.is_on_ground = True
                self.change_y = 0