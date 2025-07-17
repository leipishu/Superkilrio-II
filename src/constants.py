# constants.py
import os
from pathlib import Path

# 屏幕设置
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Superkilrio"

# 物理参数
PLAYER_SCALE = 0.5
PLAYER_SPEED = 8.0
GRAVITY = 0.98
PLAYER_JUMP_SPEED = 15.0
MAX_EXTRA_JUMPS = 1  # 二段跳设置
GROUND_HEIGHT = 130
PLAYER_MAX_HEALTH = 200  # 玩家最大生命值

# 攻击系统
ATTACK_COOLDOWN = 0.3  # 攻击冷却时间(秒)
ATTACK_RANGE = 80  # 攻击范围(像素)
ATTACK_DAMAGE = 50
ATTACK_ANIMATION_SPEED = 0.1  # 攻击动画速度

# NPC
NPC_SCALE = 0.5
TRAINER_DIALOGUE_COOLDOWN = 2.0  # 对话冷却时间

# Enemies
ENEMY_SCALE = 0.5      # 敌人基础缩放

# 地面设置
GROUND_Y = 130  # 地面线位置（从屏幕底部算起）

# 路径处理
PROJECT_ROOT = Path(__file__).parent.parent
def get_asset_path(relative_path: str) -> str:
    """自动补全资源路径"""
    return str(PROJECT_ROOT / "src" / "assets" / relative_path)