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
        elif key == arcade.key.SPACE:
            if self.game.level_manager.current_level.is_completed:
                self.game.level_manager.next_level(player=self.game.player)
        elif key == arcade.key.F1:
            # 手动切换到关卡1进行测试
            self.game.level_manager.goto_level(1, player=self.game.player)
        elif key == arcade.key.F3:
            self.game.debug_mode = not self.game.debug_mode

        # 处理交互
        self.game.interaction_system.handle_interaction(key)

    def on_key_release(self, key, modifiers):
        """键盘释放事件"""
        if key in self.game.held_keys:
            self.game.held_keys.remove(key)
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.game.player.change_x = 0