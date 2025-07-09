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

    def handle_interaction(self, key):
        """处理交互按键"""
        if key == arcade.key.E and self.near_npc:
            if not self.game.dialogue_system.is_visible:
                if hasattr(self.near_npc, 'get_dialogue'):
                    self.game.dialogue_system.start_dialogue(self.near_npc.get_dialogue())
            else:
                if self.game.dialogue_system.next_line():
                    self.game.logger.debug("Dialogue ended")