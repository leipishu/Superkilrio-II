import arcade
from src.constants import *

class TrainerNPC(arcade.Sprite):
    def __init__(self):
        # 完全模仿player.py的加载方式
        super().__init__()
        
        # 调整为与player相同尺寸
        self.scale = NPC_SCALE  # 修改点1：使用统一缩放比例
        
        # 加载纹理（仅站立状态）
        try:
            assets_dir = get_asset_path("npc")
            self.texture = arcade.load_texture(f"{assets_dir}/trainer.png")
            print("✅ NPC纹理加载成功")
        except Exception as e:
            print(f"⚠️ NPC纹理加载失败: {str(e)}")
            # 备用方案：红色方块
            self.color = arcade.color.RED
            print("🟥 使用红色替代方块")