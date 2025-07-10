# src/ecs/entities/enemies/level1_grunt.py
import arcade
import os
from src.constants import *
from src.utils.logging_config import logger


class Level1Grunt(arcade.Sprite):
    """一级步兵实体（包含站立和跑步动画）"""

    def __init__(self):
        super().__init__()
        self.logger = logger.getChild("Level1Grunt")
        self.scale = ENEMY_SCALE  # 从constants.py导入

        # 动画控制
        self.run_frames = []
        self.stand_texture = None
        self.current_frame = 0
        self.animation_speed = 0.1
        self.time_since_last_frame = 0
        self.is_running = False

        # 物理属性
        self.health = 100
        self.speed = 2.0
        self.enemy_level = 1
        self.facing_right = False

        # 加载纹理
        self.load_textures()

        # 初始化状态
        if self.stand_texture:
            self.texture = self.stand_texture
            self.set_hit_box(self.texture.hit_box_points)
        else:
            self.setup_fallback()

        self.logger.info("一级步兵初始化完成")

    def load_textures(self):
        """加载所有需要的纹理"""
        try:
            assets_dir = get_asset_path("enemies/level1_grunt")

            # 加载站立纹理
            stand_path = os.path.join(assets_dir, "stand.png")
            self.stand_texture = arcade.load_texture(stand_path)

            # 加载跑步动画帧 (run_1.png到run_6.png)
            self.run_frames = [
                arcade.load_texture(os.path.join(assets_dir, f"run_{i}.png"))
                for i in range(1, 7)  # 假设6帧动画
            ]

            self.logger.debug(f"加载了{len(self.run_frames)}帧跑步动画和站立纹理")

        except Exception as e:
            self.logger.error(f"纹理加载失败: {str(e)}")
            self.stand_texture = None
            self.run_frames = []

    def setup_fallback(self):
        """备用纹理方案"""
        self.color = arcade.color.RED
        self.width = 60
        self.height = 80
        self.set_hit_box([[-30, -40], [30, -40], [30, 40], [-30, 40]])
        self.logger.warning("使用备用纹理")

    def update_animation(self, delta_time: float):
        """更新动画状态"""
        if not self.stand_texture:
            return

        # 站立状态
        if not self.is_running or not self.run_frames:
            self.texture = self.stand_texture
            return

        # 跑步动画
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0
            self.current_frame = (self.current_frame + 1) % len(self.run_frames)
            texture = self.run_frames[self.current_frame]

            # 根据方向翻转纹理
            if self.change_x < 0 and self.facing_right:
                self.facing_right = False
                self.texture = texture.flip_horizontally()
            elif self.change_x > 0 and not self.facing_right:
                self.facing_right = True
                self.texture = texture.flip_horizontally()
            else:
                self.texture = texture

    def update(self):
        """更新逻辑（基础移动）"""
        if abs(self.change_x) > 0.1:
            self.is_running = True
        else:
            self.is_running = False