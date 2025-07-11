# src/ecs/systems/ai_system.py
from src.constants import PLAYER_JUMP_SPEED
import time
import random
from src.utils.logging_config import logger


class AISystem:
    """优化的AI系统，包含更平滑的追踪和跳跃逻辑"""

    def __init__(self):
        self.last_update_time = time.time()
        self.direction_change_cooldown = 0

    def update_entity(self, enemy, player, delta_time=0.016):
        """
        优化的AI更新方法
        :param enemy: 敌人实体
        :param player: 玩家实体
        :param delta_time: 帧时间间隔
        """
        # Remove the time-based throttling to ensure smooth movement
        # The AI should update every frame for smooth chasing

        try:
            # 获取必要属性，提供默认值
            enemy_x = getattr(enemy, 'center_x', 0)
            enemy_y = getattr(enemy, 'center_y', 0)
            player_x = getattr(player, 'center_x', 0)
            player_y = getattr(player, 'center_y', 0)

            dx = player_x - enemy_x
            dy = player_y - enemy_y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # 获取检测范围和速度
            detection_range = getattr(enemy, 'detection_range', 500)
            speed = getattr(enemy, 'speed', 2.0)

            # 检查是否在检测范围内
            if distance <= detection_range:
                # 在检测范围内 - 追踪玩家
                if abs(dx) > 5:  # 只有当距离足够远时才移动
                    if dx > 0:
                        enemy.change_x = speed
                    else:
                        enemy.change_x = -speed
                else:
                    # 当非常接近时，停止移动
                    enemy.change_x = 0

                # 更新面向方向
                if hasattr(enemy, 'facing_right'):
                    enemy.facing_right = dx > 0

                # 跳跃逻辑 - 当玩家在上方且足够接近时
                jump_ratio = getattr(enemy, 'jump_ratio', 0.7)
                if (abs(dx) < 100 and  # 足够接近
                        getattr(enemy, 'is_on_ground', False) and  # 在地面上
                        dy > 30 and  # 玩家在上方一定高度
                        random.random() < 0.005):  # 跳跃概率
                    enemy.change_y = PLAYER_JUMP_SPEED * jump_ratio
            else:
                # 超出检测范围 - 停止移动
                enemy.change_x = 0

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.warning(f"Failed to update AI for enemy {enemy.name}: {str(e)}")