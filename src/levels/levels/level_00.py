"""Level 00 implementation"""
from ..level_manager import Level as BaseLevel
from src.ecs.entities.npc.trainer import TrainerNPC
from src.constants import *
import arcade

LEVEL_NUM = 0

class Level(BaseLevel):
    """Level 00 concrete implementation"""
    def __init__(self):
        super().__init__()
        print("🆕 Level00实例创建完成")
        print(f"父类: {super().__class__.__name__}")
        print(f"初始化时npcs列表: {self.npcs} (长度: {len(self.npcs)})")

    def setup(self):
        print("🛠️ 开始setup()")
        # 创建教官NPC
        self.trainer = TrainerNPC()
        self.trainer.center_x = SCREEN_WIDTH // 2
        self.trainer.center_y = GROUND_Y + 100
        
        print(f"🎮 创建NPC: 位置({self.trainer.center_x}, {self.trainer.center_y})")
        print(f"添加前npcs列表长度: {len(self.npcs)}")
        
        self.npcs.append(self.trainer)
        
        print(f"添加后npcs列表长度: {len(self.npcs)}")
        print(f"列表内容检查: {'trainer' in [sprite.properties.get('name', '') for sprite in self.npcs]}")

        # 本关可直接通过
        self.is_completed = True

    def draw(self):
        # 仅调用父类绘制方法
        super().draw()
