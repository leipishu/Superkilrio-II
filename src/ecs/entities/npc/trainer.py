import arcade
from src.constants import *
from src.utils.logging_config import logger

class TrainerNPC(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.logger = logger.getChild("TrainerNPC")
        
        # 调整为与player相同尺寸
        self.scale = NPC_SCALE  # 修改点1：使用统一缩放比例
        
        # 加载纹理（仅站立状态）
        try:
            assets_dir = get_asset_path("npc")
            self.texture = arcade.load_texture(f"{assets_dir}/trainer.png")
            self.logger.info("NPC texture loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load NPC texture: {str(e)}")
            # 备用方案：红色方块
            self.color = arcade.color.RED
            self.logger.warning("Using fallback texture.")