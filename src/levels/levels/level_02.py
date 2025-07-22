# src/levels/levels/level_02.py
from ..level_manager import Level as BaseLevel
from src.ecs.entities.enemies.level1_grunt import Level1Grunt
from src.ecs.entities.enemies.level2_grunt import Level2Grunt  # 导入Level2Grunt
from src.constants import *
from src.utils.logging_config import logger
import random

LEVEL_NUM = 2  # 必须定义关卡编号


class Level(BaseLevel):
    """第二关实现 - 包含3个一级步兵和1个二级步兵"""

    def __init__(self):
        super().__init__()
        self.logger = logger.getChild(f"Level{LEVEL_NUM}")
        self.logger.info("Initializing Level 2")

        # 预加载敌人资源
        Level1Grunt.preload_json()
        Level2Grunt.preload_json()  # 预加载二级步兵资源

    def setup(self, player=None):
        """设置关卡内容"""
        super().setup(player)
        self.logger.info("Setting up Level 2 enemies")

        player_start_x = 100  # 玩家起始位置

        # 生成3个Level1Grunt
        for i in range(3):
            grunt = Level1Grunt()
            x = random.randint(player_start_x - 200, player_start_x + 200)
            y = GROUND_Y + grunt.height / 2

            # 防重叠
            while any(abs(x - e.center_x) < 80 for e in self.enemies):
                x = random.randint(player_start_x - 200, player_start_x + 200)

            grunt.center_x = x
            grunt.center_y = y
            grunt.change_x = 0
            self.enemies.append(grunt)

        # 生成1个Level2Grunt (放在更远的位置)
        elite = Level2Grunt()
        elite.center_x = random.randint(player_start_x + 300, player_start_x + 500)
        elite.center_y = GROUND_Y + elite.height / 2
        elite.change_x = 0
        self.enemies.append(elite)

        self.is_completed = False
        self.logger.info(f"Level 2 setup complete with {len(self.enemies)} enemies")

    def update(self, delta_time: float):
        """更新关卡逻辑"""
        super().update(delta_time)

        # 更新所有敌人
        for enemy in self.enemies:
            enemy.update()
            enemy.update_animation(delta_time)
            if hasattr(enemy, 'update_ai') and self.player:
                enemy.update_ai(self.player, delta_time)

        # 检查关卡是否完成
        if len(self.enemies) == 0:
            self.is_completed = True

    def draw(self):
        """绘制关卡内容"""
        super().draw()  # 绘制基础内容
        # 可以添加第二关特有的绘制内容