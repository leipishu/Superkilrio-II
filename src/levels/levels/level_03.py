# src/levels/levels/level_03.py
from ..level_manager import Level as BaseLevel
from src.ecs.entities.enemies.level1_grunt import Level1Grunt  # 导入Level1Grunt
from src.ecs.entities.enemies.level2_grunt import Level2Grunt  # 导入Level2Grunt
from src.ecs.entities.enemies.level3_grunt import Level3Grunt  # 导入Level3Grunt
from src.constants import *
from src.utils.logging_config import logger
import random

LEVEL_NUM = 3  # 必须定义关卡编号


class Level(BaseLevel):
    """第三关实现 - 包含5个一级步兵和2个二级步兵和1个三级步兵"""

    def __init__(self):
        super().__init__()
        self.logger = logger.getChild(f"Level{LEVEL_NUM}")
        self.logger.info("Initializing Level 3")

        # 预加载敌人资源
        Level1Grunt.preload_json()
        Level2Grunt.preload_json()  # 预加载二级步兵资源

    def setup(self, player=None):
        """设置关卡内容（优化版）"""
        super().setup(player)
        self.logger.info("Setting up Level 3 enemies")

        player_start_x = 100  # 玩家起始位置
        spawn_attempts = 0
        max_attempts = 100  # 最大尝试次数防止死循环

        for i in range(5):
            grunt = Level1Grunt()
            spawn_success = False
            spawn_attempts = 0

            while not spawn_success and spawn_attempts < max_attempts:
                x = random.randint(player_start_x - 200, player_start_x + 200)
                y = GROUND_Y + grunt.height / 2

                # 检查与现有敌人的距离
                if not self.enemies or all(abs(x - e.center_x) >= 80 for e in self.enemies):
                    grunt.center_x = x
                    grunt.center_y = y
                    grunt.change_x = 0
                    self.enemies.append(grunt)
                    spawn_success = True
                    self.logger.debug(f"Spawned Level1Grunt at ({x}, {y})")

                spawn_attempts += 1

            if not spawn_success:
                self.logger.warning("Failed to spawn Level1Grunt after 100 attempts")

        for j in range(2):
            grunt = Level2Grunt()
            spawn_success = False
            spawn_attempts = 0

            while not spawn_success and spawn_attempts < max_attempts:
                x = random.randint(player_start_x - 200, player_start_x + 200)
                y = GROUND_Y + grunt.height / 2

                # 放宽距离要求到60像素
                if not self.enemies or all(abs(x - e.center_x) >= 60 for e in self.enemies):
                    grunt.center_x = x
                    grunt.center_y = y
                    grunt.change_x = 0
                    self.enemies.append(grunt)
                    spawn_success = True
                    self.logger.debug(f"Spawned Level2Grunt at ({x}, {y})")

                spawn_attempts += 1

            if not spawn_success:
                # 尝试在更远位置生成
                x = random.choice([random.randint(player_start_x - 400, player_start_x - 250),
                                   random.randint(player_start_x + 250, player_start_x + 400)])
                grunt.center_x = x
                grunt.center_y = GROUND_Y + grunt.height / 2
                self.enemies.append(grunt)
                self.logger.warning(f"Using fallback spawn position for Level2Grunt at ({x}, {y})")

        elite = Level3Grunt()
        elite_spawned = False

        # 优先尝试在右侧生成
        for x in [player_start_x + 300, player_start_x + 350, player_start_x + 400]:
            if all(abs(x - e.center_x) >= 100 for e in self.enemies):
                elite.center_x = x
                elite.center_y = GROUND_Y + elite.height / 2
                elite.change_x = 0
                self.enemies.append(elite)
                elite_spawned = True
                self.logger.debug(f"Spawned Level3Grunt at ({x}, {y})")
                break

        if not elite_spawned:
            # 强制生成在最右侧
            elite.center_x = player_start_x + 500
            elite.center_y = GROUND_Y + elite.height / 2
            self.enemies.append(elite)
            self.logger.warning("Level3Grunt forced to spawn at far right position")

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