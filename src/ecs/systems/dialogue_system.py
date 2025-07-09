# src/ecs/systems/dialogue_system.py
import arcade
from typing import Optional, List
from src.constants import *


class DialogueSystem:
    """处理所有NPC对话交互的核心系统"""

    def __init__(self):
        self.active_dialogue: Optional[List[str]] = None
        self.current_line = 0
        self.box_height = 150
        self.box_color = arcade.color.DARK_SLATE_GRAY
        self.text_color = arcade.color.WHITE
        self.is_visible = False

    def start_dialogue(self, lines: List[str]):
        """开始一段新对话"""
        self.active_dialogue = lines
        self.current_line = 0
        self.is_visible = True

    def next_line(self) -> bool:
        """推进到下一条对话，返回是否对话结束"""
        if not self.active_dialogue:
            return True

        self.current_line += 1
        if self.current_line >= len(self.active_dialogue):
            self.end_dialogue()
            return True
        return False

    def end_dialogue(self):
        """结束当前对话"""
        self.active_dialogue = None
        self.is_visible = False

    def draw(self):
        """绘制对话界面"""
        if not self.is_visible or not self.active_dialogue:
            return

        # 绘制对话背景框
        arcade.draw_rectangle_filled(
            center_x=SCREEN_WIDTH // 2,
            center_y=self.box_height // 2,
            width=SCREEN_WIDTH,
            height=self.box_height,
            color=self.box_color
        )

        # 绘制当前对话文本
        arcade.draw_text(
            text=self.active_dialogue[self.current_line],
            start_x=50,
            start_y=40,
            color=self.text_color,
            font_size=20,
            width=SCREEN_WIDTH - 100,
            font_name="Microsoft YaHei"
        )

        # 修改：将提示按键改为E键
        arcade.draw_text(
            text="按E键继续...",
            start_x=SCREEN_WIDTH - 150,
            start_y=20,
            color=arcade.color.LIGHT_GRAY,
            font_size=14
        )