# src/systems/renderer.py
import arcade
from src.constants import *
from src.items.dropped_item import DroppedItem

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

        # 绘制玩家血条
        self._draw_player_health_bar()

        # 绘制对话系统
        self.game.dialogue_system.draw()

        # 绘制粒子
        self.game.combat_system.particle_system.draw()

        # 绘制物品栏
        self._draw_inventory()

        # 绘制拾取提示
        self._draw_pickup_prompt()

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

    def _draw_player_health_bar(self):
        """右上角绘制玩家血条"""
        player = self.game.player
        bar_width = 300
        bar_height = 28
        margin = 30
        x = SCREEN_WIDTH - bar_width - margin
        y = SCREEN_HEIGHT - bar_height - margin
        # 背景
        arcade.draw_rectangle_filled(x + bar_width/2, y + bar_height/2, bar_width, bar_height, arcade.color.DARK_GRAY)
        # 血量
        health_ratio = player.health / player.max_health
        health_width = int(bar_width * health_ratio)
        arcade.draw_rectangle_filled(x + health_width/2, y + bar_height/2, health_width, bar_height-6, arcade.color.RED)
        # 边框
        arcade.draw_rectangle_outline(x + bar_width/2, y + bar_height/2, bar_width, bar_height, arcade.color.WHITE, 2)
        # 数值
        arcade.draw_text(f"HP: {player.health}/{player.max_health}", x + 10, y + 2, arcade.color.WHITE, 18, font_name=self.game.font_name)

    def _draw_inventory(self):
        """绘制物品栏"""
        player = self.game.player

        # 计算物品栏总宽度和起始位置(居中)
        total_width = (INVENTORY_SLOT_SIZE * INVENTORY_SLOT_COUNT +
                       INVENTORY_SLOT_MARGIN * (INVENTORY_SLOT_COUNT - 1))
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = SCREEN_HEIGHT - INVENTORY_SLOT_SIZE - 20  # 顶部留20像素边距

        # 绘制背景条
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2, y + INVENTORY_SLOT_SIZE // 2,
            total_width + 20, INVENTORY_SLOT_SIZE + 20,
            INVENTORY_BACKGROUND_COLOR
        )

        # 绘制所有格子
        for i in range(INVENTORY_SLOT_COUNT):
            x = start_x + i * (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_MARGIN)

            # 绘制格子背景
            color = INVENTORY_SLOT_SELECTED_COLOR if i == player.selected_slot else INVENTORY_SLOT_COLOR
            arcade.draw_rectangle_filled(
                x + INVENTORY_SLOT_SIZE // 2,
                y + INVENTORY_SLOT_SIZE // 2,
                INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE,
                color
            )

            # 绘制格子边框
            arcade.draw_rectangle_outline(
                x + INVENTORY_SLOT_SIZE // 2,
                y + INVENTORY_SLOT_SIZE // 2,
                INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE,
                arcade.color.BLACK, 2
            )

            # 绘制物品(如果有)
            if player.inventory[i]:
                item = player.inventory[i]
                item_sprite = arcade.Sprite()
                item_sprite.texture = item.texture
                item_sprite.scale = min(
                    INVENTORY_SLOT_SIZE / item_sprite.texture.width * 0.8,
                    INVENTORY_SLOT_SIZE / item_sprite.texture.height * 0.8
                )
                item_sprite.center_x = x + INVENTORY_SLOT_SIZE // 2
                item_sprite.center_y = y + INVENTORY_SLOT_SIZE // 2
                item_sprite.draw()

    def _draw_pickup_prompt(self):
        """绘制拾取提示"""
        # 检查玩家附近是否有可拾取物品
        for item in self.game.level_manager.current_level.items:
            if isinstance(item, DroppedItem) and arcade.check_for_collision(self.game.player, item):
                # 在玩家头顶显示提示
                arcade.draw_text(
                    "按F拾取",
                    self.game.player.center_x,
                    self.game.player.top + 20,
                    arcade.color.WHITE,
                    font_size=16,
                    font_name="Microsoft YaHei",
                    anchor_x="center"
                )
                break