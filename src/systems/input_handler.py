# src/systems/input_handler.py
from src.constants import *
import arcade


class InputHandler:
    def __init__(self, game_controller):
        self.game = game_controller

    def on_key_press(self, key, modifiers):
        """键盘按下事件"""
        self.game.held_keys.add(key)

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.game.player.change_x = -PLAYER_SPEED
            self.game.player.facing_right = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.game.player.change_x = PLAYER_SPEED
            self.game.player.facing_right = True
        elif key == arcade.key.UP or key == arcade.key.W:
            if self.game.player.is_on_ground or self.game.player.remaining_jumps > 0:
                self.game.player.change_y = PLAYER_JUMP_SPEED
                if not self.game.player.is_on_ground:
                    self.game.player.remaining_jumps -= 1
        elif key == arcade.key.Z:  # 新增攻击键
            self.game.player.try_attack()
        elif key == arcade.key.SPACE:
            if self.game.level_manager.current_level.is_completed and not self.game.dialogue_system.is_visible:
                self.game.level_manager.next_level(player=self.game.player)
        elif key == arcade.key.F1:
            # 手动切换到关卡1进行测试
            self.game.level_manager.goto_level(3, player=self.game.player)
        elif key == arcade.key.F3:
            self.game.debug_mode = not self.game.debug_mode
        elif key == arcade.key.KEY_1:  # 数字键快速选择格子
            self.game.player.selected_slot = 0
        elif key == arcade.key.KEY_2:
            self.game.player.selected_slot = 1
        elif key == arcade.key.KEY_3:
            self.game.player.selected_slot = 2
        elif key == arcade.key.KEY_4:
            self.game.player.selected_slot = 3
        elif key == arcade.key.KEY_5:
            self.game.player.selected_slot = 4
        elif key == arcade.key.KEY_6:
            self.game.player.selected_slot = 5
        elif key == arcade.key.KEY_7:
            self.game.player.selected_slot = 6
        elif key == arcade.key.KEY_8:
            self.game.player.selected_slot = 7
        elif key == arcade.key.KEY_9:
            self.game.player.selected_slot = 8
        elif key == arcade.key.F:  # 使用当前选中物品
            selected_item = self.game.player.inventory[self.game.player.selected_slot]
            if selected_item and hasattr(selected_item, 'use'):
                selected_item.use(self.game.player)
        elif key == arcade.key.E:  # 使用F键拾取物品
            self.game.interaction_system.check_item_pickup()
        elif key == arcade.key.Q:  # 丢弃当前选中物品
            dropped_item = self.game.player.drop_item(self.game.player.selected_slot)
            if dropped_item:
                # 确保当前关卡有物品列表
                if not hasattr(self.game.level_manager.current_level, 'items'):
                    self.game.level_manager.current_level.items = arcade.SpriteList()
                self.game.level_manager.current_level.items.append(dropped_item)

        # 处理交互
        self.game.interaction_system.handle_interaction(key)

    def on_key_release(self, key, modifiers):
        """键盘释放事件"""
        if key in self.game.held_keys:
            self.game.held_keys.remove(key)
        if key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.game.player.change_x = 0