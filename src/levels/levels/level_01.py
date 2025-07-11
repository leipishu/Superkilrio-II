# src/levels/levels/level_01.py
from ..level_manager import Level as BaseLevel
from src.ecs.entities.enemies.level1_grunt import Level1Grunt
from src.constants import *
from src.utils.logging_config import logger
import random

LEVEL_NUM = 1  # 必须定义


class Level(BaseLevel):  # 类名必须为Level，不是Level01
    """第一关实现"""

    def __init__(self):
        super().__init__()
        self.logger = logger.getChild(f"Level{LEVEL_NUM}")
        self.logger.info("Setting up level")
        self.change_y = 0  # 初始垂直速度
        self.change_x = 0  # 初始水平速度
        self.player = None  # 新增：存储玩家引用

    def setup(self, player=None):  # 修改：添加player参数
        """设置关卡内容"""
        super().setup(player)  # Call parent setup to store player reference
        self.logger.info("Setting up Level1")

        # 生成3个随机位置的敌人 - 更靠近玩家起始位置
        player_start_x = 100  # 玩家起始位置
        for i in range(3):
            grunt = Level1Grunt()
            # 在玩家附近生成敌人，确保在检测范围内
            x = random.randint(player_start_x - 200, player_start_x + 200)
            y = GROUND_Y + grunt.height / 2

            # 防重叠
            while any(abs(x - e.center_x) < 80 for e in self.enemies):
                x = random.randint(player_start_x - 200, player_start_x + 200)

            grunt.center_x = x
            grunt.center_y = y
            grunt.change_x = 0  # 初始不移动，让AI控制
            self.enemies.append(grunt)

        self.is_completed = False
        self.logger.info("Level1 Initialized")

    def update(self, delta_time: float):
        """更新关卡逻辑"""
        super().update(delta_time)

        # 确保所有敌人都被更新
        for enemy in self.enemies:
            enemy.update()  # 更新基础移动
            enemy.update_animation(delta_time)  # 更新动画
            if hasattr(enemy, 'update_ai') and self.player:
                enemy.update_ai(self.player, delta_time)

        if len(self.enemies) == 0:
            self.is_completed = True

    def draw(self):
        """绘制关卡"""
        super().draw()  # 绘制敌人等基础内容
        # 可添加关卡特定的绘制内容