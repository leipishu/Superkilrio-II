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

    def get_dialogue(self):
        """返回NPC的对话内容"""
        return [
            "博士（语气低沉）：欢迎来到这个被遗忘的世界，旅者。在很久以前，我们曾站在科技的巅峰，触摸到了时间的奥秘。\n然而，就在我们以为能够改变一切的时候，一群自称为“高级文明”的存在降临了。",
            "博士（的语气中带着一丝愤怒）：他们嘲笑我们是“低级文明”，夺走了我们的时光机，抹去了众人的记忆，只留下我，\n让我独自面对这个破碎的世界。他们说我们不配拥有这样的力量，但我知道，这只是他们害怕我们崛起的借口！",
            "博士（眼神变得坚定）：但我从未放弃。我用尽一生的时间，寻找那些散落在世界各地的宇航飞船残骸，收集它们的碎片，\n试图重建我们的荣耀。现在，这一切都交给你了。你必须踏上旅程，收集那些失落的碎片，解开时光机的秘密，\n证明我们有能力掌握自己的命运！",
            "博士（凝视着你）：记住，你的选择将决定一切。你的路途不会轻松，你面对的敌人会越来越强，但你必须勇敢前行。\n你必须去战斗，去证明，去夺回属于我们的未来！祝你好运，旅者。"
        ]