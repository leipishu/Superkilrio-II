# src/ecs/systems/ai_system.py
from src.constants import PLAYER_JUMP_SPEED
import time


class AISystem:
    """最终修正的AI系统，正确处理delta_time参数"""

    def __init__(self):
        self.last_update_time = time.time()  # 初始化时间记录

    def update_entity(self, enemy, player, delta_time=0.016):
        """
        最终修正的AI更新方法
        :param enemy: 敌人实体
        :param player: 玩家实体
        :param delta_time: 帧时间间隔(默认60FPS的帧时间)
        """
        try:
            # 防抖控制(100ms更新一次)
            current_time = time.time()
            if current_time - self.last_update_time < 0.1:
                return
            self.last_update_time = current_time

            # 安全获取坐标值
            player_x = getattr(player, 'center_x', 0)
            enemy_x = getattr(enemy, 'center_x', 0)
            dx = player_x - enemy_x

            # 追踪逻辑
            if abs(dx) < getattr(enemy, 'detection_range', 300):
                speed = getattr(enemy, 'speed', 2.0)
                enemy.change_x = speed if dx > 0 else -speed

                # 更新面向方向
                if hasattr(enemy, 'facing_right'):
                    enemy.facing_right = dx > 0

                # 跳跃逻辑
                if (abs(dx) < 100 and
                        getattr(enemy, 'is_on_ground', False) and
                        getattr(player, 'center_y', 0) > getattr(enemy, 'center_y', 0)):
                    enemy.change_y = PLAYER_JUMP_SPEED * getattr(enemy, 'jump_ratio', 0.7)
            else:
                enemy.change_x = 0

        except Exception as e:
            print(f"AI更新出错: {str(e)}")