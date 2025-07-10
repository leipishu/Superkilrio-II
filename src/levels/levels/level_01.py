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
        self.logger.info("初始化Level1")
        self.change_y = 0  # 初始垂直速度
        self.change_x = 0  # 初始水平速度

    def setup(self):
        self.logger.info("设置Level1关卡")

        # 生成3个随机位置的敌人
        for i in range(3):
            grunt = Level1Grunt()
            x = random.randint(200, SCREEN_WIDTH - 200)
            y = GROUND_Y + grunt.height / 2

            # 防重叠
            while any(abs(x - e.center_x) < 150 for e in self.enemies):
                x = random.randint(200, SCREEN_WIDTH - 200)

            grunt.center_x = x
            grunt.center_y = y
            grunt.change_x = random.choice([-1, 1]) * grunt.speed
            self.enemies.append(grunt)

        self.is_completed = False
        self.logger.info("Level1设置完成")

    def spawn_grunts(self, count: int):
        """生成指定数量的一级步兵"""
        for i in range(count):
            try:
                grunt = Level1Grunt()

                # 随机位置（确保在地面上且不重叠）
                x = random.randint(200, SCREEN_WIDTH - 200)
                y = GROUND_Y + grunt.height / 2

                # 确保不与现有敌人重叠
                while any(abs(x - e.center_x) < 100 for e in self.enemies):
                    x = random.randint(200, SCREEN_WIDTH - 200)

                grunt.center_x = x
                grunt.center_y = y

                # 随机初始移动方向
                grunt.change_x = random.choice([-1, 1]) * grunt.speed

                self.enemies.append(grunt)
                self.logger.debug(f"生成一级步兵 {i + 1} 在 ({x}, {y})")

            except Exception as e:
                self.logger.error(f"生成一级步兵失败: {str(e)}")

    def update(self, delta_time: float):
        """更新关卡逻辑"""
        super().update(delta_time)  # 调用父类物理更新

        # 检查关卡完成条件
        if len(self.enemies) == 0:
            self.is_completed = True
            self.logger.info("所有敌人都被击败，关卡完成")

    def draw(self):
        """绘制关卡"""
        super().draw()  # 绘制敌人等基础内容
        # 可添加关卡特定的绘制内容