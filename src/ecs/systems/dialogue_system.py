# src/ecs/systems/dialogue_system.py
import arcade
from typing import List, Optional
from src.constants import SCREEN_WIDTH


class DialogueSystem:
    """改进版对话系统，支持长文本自动换行"""

    def __init__(self):
        self.active_dialogue: Optional[List[str]] = None
        self.current_line = 0
        self.box_height = 200  # 增加对话框高度
        self.box_color = (240, 240, 240, 230)  # 半透明白色 (RGBA)
        self.text_color = arcade.color.BLACK
        self.border_color = arcade.color.DARK_GRAY
        self.is_visible = False
        self.font_name = "Microsoft YaHei"
        self.font_size = 18
        self.line_height = 36  # 行高
        self.margin = 30
        self.max_line_width = SCREEN_WIDTH - 2 * self.margin

    def start_dialogue(self, lines: List[str]):
        """开始对话时自动分割长文本"""
        self.active_dialogue = []
        for line in lines:
            # 自动分割过长的单行文本
            wrapped_lines = self._wrap_text(line)
            self.active_dialogue.extend(wrapped_lines)
        self.current_line = 0
        self.is_visible = True

    def _wrap_text(self, text: str) -> List[str]:
        """手动实现文本换行逻辑"""
        words = text.split(' ')
        lines = []
        current_line = []
        current_line_width = 0

        for word in words:
            # 估算单词宽度（近似值）
            word_width = len(word) * self.font_size * 0.6

            if current_line and (current_line_width + word_width > self.max_line_width):
                lines.append(' '.join(current_line))
                current_line = [word]
                current_line_width = word_width
            else:
                current_line.append(word)
                current_line_width += word_width + self.font_size * 0.3  # 加空格宽度

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def next_line(self) -> bool:
        """推进到下一条对话"""
        if not self.active_dialogue:
            return True

        self.current_line += 1
        if self.current_line >= len(self.active_dialogue):
            self.end_dialogue()
            return True
        return False

    def end_dialogue(self):
        """结束对话"""
        self.active_dialogue = None
        self.is_visible = False

    def draw(self):
        """绘制带自动换行的对话界面"""
        if not self.is_visible or not self.active_dialogue:
            return

        # 绘制半透明背景框
        arcade.draw_rectangle_filled(
            center_x=SCREEN_WIDTH // 2,
            center_y=self.box_height // 2,
            width=SCREEN_WIDTH,
            height=self.box_height,
            color=self.box_color
        )

        # 绘制边框
        arcade.draw_rectangle_outline(
            center_x=SCREEN_WIDTH // 2,
            center_y=self.box_height // 2,
            width=SCREEN_WIDTH - 10,
            height=self.box_height - 10,
            color=self.border_color,
            border_width=2
        )

        # 绘制当前对话文本（手动实现多行绘制）
        current_text = self.active_dialogue[self.current_line]
        y_position = self.box_height - self.margin - self.font_size

        # 如果文本包含换行符，则分割成多行
        for line in current_text.split('\n'):
            arcade.draw_text(
                text=line,
                start_x=self.margin,
                start_y=y_position,
                color=self.text_color,
                font_size=self.font_size,
                width=self.max_line_width,
                font_name=self.font_name,
                align="left"
            )
            y_position -= self.line_height

        # 绘制页码指示器
        page_indicator = f"{self.current_line + 1}/{len(self.active_dialogue)}"
        arcade.draw_text(
            text=page_indicator,
            start_x=SCREEN_WIDTH - self.margin - 50,
            start_y=20,
            color=arcade.color.DARK_GRAY,
            font_size=14,
            font_name=self.font_name
        )

        # 绘制继续提示
        arcade.draw_text(
            text="按E键继续...",
            start_x=self.margin,
            start_y=20,
            color=arcade.color.DARK_GRAY,
            font_size=14,
            font_name=self.font_name
        )