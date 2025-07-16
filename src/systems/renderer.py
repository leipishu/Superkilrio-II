# src/systems/renderer.py
import arcade
from src.constants import *

class Renderer:
    def __init__(self, game_controller):
        self.game = game_controller

    def draw(self):
        """渲染游戏画面"""
        arcade.start_render()

        # 绘制背景
        if self.game.background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                self.game.background
            )

        # 绘制地面
        arcade.draw_line(0, GROUND_Y, SCREEN_WIDTH, GROUND_Y, arcade.color.BLACK, 3)

        # 绘制关卡内容
        self.game.level_manager.draw()

        # 绘制玩家
        self.game.player.draw()

        # 绘制对话系统
        self.game.dialogue_system.draw()

        # 绘制粒子
        self.game.combat_system.particle_system.draw()

        # 调试信息
        if self.game.debug_mode:
            self._draw_debug_info()
            # 绘制NPC交互提示
            if self.game.interaction_system.near_npc and not self.game.dialogue_system.is_visible:
                arcade.draw_text(
                    "按E键交互",
                    self.game.interaction_system.near_npc.center_x,
                    self.game.interaction_system.near_npc.top + 20,
                    arcade.color.WHITE,
                    font_size=16,
                    font_name="Microsoft YaHei",
                    anchor_x="center"
                )

    def _draw_debug_info(self):
        """绘制调试信息"""
        arcade.draw_text(
            f"Level: {self.game.level_manager.current_level_num}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 20,
            font_name=self.game.font_name
        )