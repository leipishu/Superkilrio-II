# src/systems/interaction_system.py
import math
import arcade
from src.constants import *

class InteractionSystem:
    def __init__(self, game_controller):
        self.game = game_controller
        self.near_npc = None

    def check_npc_proximity(self):
        """检查玩家是否接近NPC"""
        self.near_npc = None
        if self.game.level_manager.current_level and hasattr(self.game.level_manager.current_level, 'npcs'):
            for npc in self.game.level_manager.current_level.npcs:
                distance = math.sqrt(
                    (self.game.player.center_x - npc.center_x) ** 2 +
                    (self.game.player.center_y - npc.center_y) ** 2
                )
                if distance <= 100:  # 交互距离
                    self.near_npc = npc
                    break

    def check_item_pickup(self):
        if not hasattr(self.game.player, 'center_x'):
            return

        for item in self.game.level_manager.current_level.items:
            # 精确碰撞检测
            if arcade.check_for_collision(self.game.player, item):
                if hasattr(item, 'item_data'):
                    if item.item_data.use(self.game.player):
                        item.remove_from_sprite_lists()
                        # 添加拾取特效
                        self.game.particle_system.create_effect(
                            item.center_x, item.center_y,
                            color=arcade.color.GOLD
                        )

    def handle_interaction(self, key):
        """处理交互按键"""
        if key == arcade.key.E and self.near_npc:
            if not self.game.dialogue_system.is_visible:
                if hasattr(self.near_npc, 'get_dialogue'):
                    self.game.dialogue_system.start_dialogue(self.near_npc.get_dialogue())
            else:
                if self.game.dialogue_system.next_line():
                    self.game.logger.debug("Dialogue ended")