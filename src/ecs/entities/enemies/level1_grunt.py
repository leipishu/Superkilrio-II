# src/ecs/entities/enemies/level1_grunt.py
import arcade
import os
from PIL.Image import FLIP_LEFT_RIGHT
from src.constants import *
from src.utils.logging_config import logger
from src.ecs.systems.ai_system import AISystem  # 新增导入
import random


class Level1Grunt(arcade.Sprite):
    """一级步兵实体（包含站立和跑步动画）"""

    def __init__(self):
        super().__init__()
        self.logger = logger.getChild("Level1Grunt")
        self.scale = ENEMY_SCALE  # 从constants.py导入

        # 动画控制 - 与玩家相同的设置
        self.run_frames = []
        self.stand_texture = None
        self.current_frame = random.randint(0, 5)  # 随机初始帧，假设6帧
        self.time_since_last_frame = random.uniform(0, 5)  # 随机初始计时器
        self.is_running = False

        # 物理属性
        self.health = 100
        self.speed = 3.0  # 增加速度让敌人移动更明显
        self.enemy_level = 1
        self.facing_right = False

        # AI相关属性
        self.ai_system = AISystem()  # 新增AI系统实例
        self.detection_range = 500  # 增加检测范围
        self.jump_ratio = 0.7  # 新增跳跃比例
        self.is_on_ground = False  # 新增地面检测

        # 加载纹理
        self.load_textures()

        # 初始化状态
        if self.stand_texture:
            self.texture = self.stand_texture
            self.set_hit_box(self.texture.hit_box_points)
        else:
            self.setup_fallback()

        self.logger.info("level1 grunt initialized")

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
        """更新动画状态 - 使用与玩家相同的动画逻辑"""
        if not self.stand_texture or not self.run_frames:
            return

        # 检测是否在地面上
        self.is_on_ground = (self.bottom <= GROUND_Y and self.change_y == 0)

        # 动画逻辑 - 与玩家相同
        if self.change_y > 0:
            # 跳跃状态 - 使用站立纹理（敌人没有跳跃纹理）
            self.texture = self.stand_texture
        elif abs(self.change_x) < 0.1:
            # 站立状态
            self.texture = self.stand_texture
        else:
            # 跑步动画
            self.time_since_last_frame += delta_time * 60  # 与玩家相同的帧率
            frames_per_texture = 5  # 与玩家相同的帧数
            
            if self.time_since_last_frame >= frames_per_texture:
                self.time_since_last_frame = 0
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                texture = self.run_frames[self.current_frame]
                
                # 根据方向翻转纹理 - 使用与玩家相同的翻转逻辑
                if not self.facing_right:
                    flipped = texture.image.transpose(FLIP_LEFT_RIGHT)
                    self.texture = arcade.Texture(f"{texture.name}_flipped", flipped)
                else:
                    self.texture = texture

    def update(self):
        """更新逻辑（基础移动）"""
        # 更新运行状态 - 与玩家相同的逻辑
        if abs(self.change_x) > 0.1:
            self.is_running = True
        else:
            self.is_running = False

        # 更新地面状态
        self.is_on_ground = (self.bottom <= GROUND_Y and self.change_y == 0)
        
        # 确保敌人不会超出屏幕边界
        if self.left < 0:
            self.left = 0
            self.change_x = abs(self.change_x)  # 反弹
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
            self.change_x = -abs(self.change_x)  # 反弹

    def update_ai(self, player, delta_time: float):
        """更新AI行为"""
        self.ai_system.update_entity(
            enemy=self,
            player=player,
            delta_time=delta_time
        )