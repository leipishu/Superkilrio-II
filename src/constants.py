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

# NPC
NPC_SCALE = 0.5
TRAINER_DIALOGUE_COOLDOWN = 2.0  # 对话冷却时间

# Enemies
ENEMY_SCALE = 0.5      # 敌人基础缩放
LEVEL1_GRUNT = {
    'health': 100,
    'speed': 2.0,
    'damage': 10,
    'ai_type': 'chase',  # AI类型
    'detection_range': 300,
    'jump_ratio': 0.7,
    'animation_speed': 0.1,
    'scale': 0.5
}

# 地面设置
GROUND_Y = 130  # 地面线位置（从屏幕底部算起）

# 路径处理
PROJECT_ROOT = Path(__file__).parent.parent
def get_asset_path(relative_path: str) -> str:
    """自动补全资源路径"""
    return str(PROJECT_ROOT / "src" / "assets" / relative_path)