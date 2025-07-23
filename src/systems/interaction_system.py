# src/systems/interaction_system.py
import math
import arcade
from src.constants import *
from src.items.dropped_item import DroppedItem

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
        """检查并拾取地上的掉落物到当前选中格子"""
        if not hasattr(self.game.player, 'center_x') or not hasattr(self.game.level_manager.current_level, 'items'):
            return

        # 检查所有掉落物
        for item in self.game.level_manager.current_level.items[:]:  # 使用副本遍历
            if isinstance(item, DroppedItem) and arcade.check_for_collision(self.game.player, item):
                # 直接放入当前选中格子（替换原有物品）
                self.game.player.inventory[self.game.player.selected_slot] = item.item_data
                item.remove_from_sprite_lists()

                # 添加拾取特效
                self.game.combat_system.particle_system.create_hit_effect(
                    item.center_x, item.center_y
                )
                break  # 一次只拾取一个物品

    def handle_interaction(self, key):
        """处理交互按键"""
        if key == arcade.key.E and self.near_npc:
            if not self.game.dialogue_system.is_visible:
                if hasattr(self.near_npc, 'get_dialogue'):
                    self.game.dialogue_system.start_dialogue(self.near_npc.get_dialogue())
            else:
                if self.game.dialogue_system.next_line():
                    self.game.logger.debug("Dialogue ended")