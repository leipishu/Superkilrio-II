import arcade
import importlib
from pathlib import Path
from typing import Dict, Type
from src.constants import *


class Level:
    """关卡基类"""

    def __init__(self):
        self.enemies = arcade.SpriteList()
        self.npcs = arcade.SpriteList()
        self.is_completed = False

    def setup(self):
        """初始化关卡内容"""
        pass

    def update(self, delta_time: float):
        """更新关卡逻辑"""
        # 修改点2：添加NPC物理更新
        for npc in self.npcs:
            npc.change_y -= GRAVITY
            if npc.bottom <= GROUND_Y:
                npc.bottom = GROUND_Y
                npc.change_y = 0

        if len(self.enemies) == 0:
            self.is_completed = True

    def draw(self):
        """绘制关卡内容"""
        self.enemies.draw()
        self.npcs.draw()


class LevelManager:
    def __init__(self):
        self.levels: Dict[int, Type[Level]] = {}
        self.current_level: Level = None
        self.current_level_num = -1

    def register_level(self, level_num: int, level_class: Type[Level]):
        """注册关卡类"""
        self.levels[level_num] = level_class

    def load_levels(self):
        """自动加载所有关卡"""
        levels_dir = Path(__file__).parent.parent / "levels" / "levels"
        print(f"📂 扫描关卡目录: {levels_dir}")
        
        for py_file in levels_dir.glob("level_*.py"):
            print(f"🔍 发现关卡文件: {py_file.name}")
            module_name = f"levels.levels.{py_file.stem}"
            
            try:
                module = importlib.import_module(module_name)
                print(f"✅ 成功导入模块: {module_name}")
                
                if hasattr(module, "LEVEL_NUM"):
                    print(f"🔢 关卡编号: {module.LEVEL_NUM}")
                else:
                    print("⚠️ 模块缺少LEVEL_NUM常量")
                
                if hasattr(module, "Level"):
                    level_class = module.Level
                    print(f"🏗️ 找到关卡类: {level_class.__name__}")
                    print(f"🔗 父类: {level_class.__bases__}")
                    
                    if level_class.__bases__[0].__name__ == "Level":
                        self.register_level(module.LEVEL_NUM, level_class)
                        print(f"📝 已注册关卡 {module.LEVEL_NUM}")
                    else:
                        print(f"⚠️ 忽略非标准关卡类: {level_class.__name__}")
                else:
                    print("⚠️ 模块缺少Level类")
                    
            except Exception as e:
                print(f"❌ 加载模块失败: {module_name} - {str(e)}")

    def goto_level(self, level_num: int):
        """切换到指定关卡"""
        print(f"🔄 尝试加载关卡 {level_num}")
        if level_num not in self.levels:
            raise ValueError(f"Level {level_num} not found")

        print(f"✅ 找到关卡类: {self.levels[level_num].__name__}")
        
        # 调试关卡实例化过程
        print("🆕 开始实例化关卡...")
        level_class = self.levels[level_num]
        self.current_level = level_class()
        print(f"🏗️ 关卡实例化完成: {self.current_level}")
        
        # 检查实例属性
        print(f"🔍 实例属性检查 - npcs: {hasattr(self.current_level, 'npcs')}")
        print(f"🔍 父类初始化状态: {'Level' in [base.__name__ for base in level_class.__bases__]}")
        
        print("🛠️ 调用关卡setup()方法")
        self.current_level.setup()
        
        # 深入调试NPC列表
        if hasattr(self.current_level, 'npcs'):
            print(f"🎮 当前关卡NPC数量: {len(self.current_level.npcs)}")
            print(f"🎮 npcs列表类型: {type(self.current_level.npcs)}")
            if len(self.current_level.npcs) > 0:
                for i, npc in enumerate(self.current_level.npcs):
                    print(f"   NPC{i}: 类型({type(npc)}), 位置({npc.center_x}, {npc.center_y}), 尺寸({npc.width}x{npc.height})")
            else:
                print("⚠️ npcs列表为空")
        
        self.current_level_num = level_num
        print(f"🏁 成功加载关卡 {level_num}")

    def next_level(self):
        """进入下一关"""
        self.goto_level(self.current_level_num + 1)

    def update(self, delta_time: float):
        """更新当前关卡"""
        if self.current_level:
            self.current_level.update(delta_time)

    def draw(self):
        """绘制当前关卡"""
        if self.current_level:
            self.current_level.draw()