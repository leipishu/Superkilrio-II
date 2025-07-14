import arcade
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, get_asset_path


class WelcomeScreen(arcade.View):
    def __init__(self, window, start_callback, about_callback, settings_callback):
        super().__init__(window)
        self.title = "Superkilrio II"
        self.buttons = [
            {"label": "Start Game", "center": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80), "callback": start_callback},
            {"label": "About", "center": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), "callback": about_callback},
            {"label": "Settings", "center": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80),
             "callback": settings_callback},
        ]
        self.selected_index = 0
        self.font_name = "Microsoft YaHei"
        self.button_width = 320
        self.button_height = 60
        self.button_radius = 16  # 统一圆角半径
        self.button_spacing = 20  # 按钮间隔
        self.background = None
        self.about_popup = False
        self.close_button_rect = None
        self.load_background()
        self._about_info = {
            "title": "Superkilrio II",
            "version": "v1.0.0",
            "author": "雷劈树",
            "group": [
                ("雷劈树", "开发者，策划，美术"),
                ("谦谦", "一代开发者"),
                ("星星院长", "剧情策划，测试"),
            ]
        }

    def load_background(self):
        """加载背景图片"""
        try:
            self.background = arcade.load_texture(get_asset_path("background.png"))
        except Exception as e:
            print(f"无法加载背景图片: {e}")
            self.background = None

    def _draw_rounded_rect(self, center_x, center_y, width, height, color, radius=16):
        """绘制圆角矩形"""
        # 主体矩形
        if width - 2 * radius > 0:
            arcade.draw_rectangle_filled(center_x, center_y, width - 2 * radius, height, color)
        if height - 2 * radius > 0:
            arcade.draw_rectangle_filled(center_x, center_y, width, height - 2 * radius, color)

        # 四个圆角
        arcade.draw_arc_filled(center_x - width // 2 + radius, center_y - height // 2 + radius,
                               radius * 2, radius * 2, color, 180, 270)
        arcade.draw_arc_filled(center_x + width // 2 - radius, center_y - height // 2 + radius,
                               radius * 2, radius * 2, color, 270, 360)
        arcade.draw_arc_filled(center_x - width // 2 + radius, center_y + height // 2 - radius,
                               radius * 2, radius * 2, color, 90, 180)
        arcade.draw_arc_filled(center_x + width // 2 - radius, center_y + height // 2 - radius,
                               radius * 2, radius * 2, color, 0, 90)

    def _draw_button(self, center_x, center_y, width, height, radius, label):
        """绘制纯白圆角按钮"""
        # 纯白色按钮 (R,G,B = 255,255,255)
        button_color = arcade.color.WHITE
        self._draw_rounded_rect(center_x, center_y, width, height, button_color, radius)

        # 绘制按钮文字
        arcade.draw_text(
            label,
            center_x, center_y - 16,
            arcade.color.BLACK,
            font_size=32,
            font_name=self.font_name,
            anchor_x="center"
        )

    def on_draw(self):
        arcade.start_render()
        # 绘制背景
        if self.background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background
            )

        # 绘制标题
        arcade.draw_text(
            self.title,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 180,
            arcade.color.YELLOW_ORANGE,
            font_size=64,
            font_name=self.font_name,
            anchor_x="center",
        )

        # 绘制所有纯白按钮
        for btn in self.buttons:
            self._draw_button(
                btn["center"][0], btn["center"][1],
                self.button_width, self.button_height,
                self.button_radius, btn["label"]
            )

        # 绘制关于弹窗
        if self.about_popup:
            self._draw_about_popup()

    def _draw_about_popup(self):
        # 弹窗尺寸和位置
        popup_width, popup_height = 800, 500
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2


        # 纯白圆角弹窗背景
        popup_color = arcade.color.WHITE
        self._draw_rounded_rect(center_x, center_y, popup_width, popup_height, popup_color, radius=36)

        # 标题和版本
        title_y = center_y + popup_height // 2 - 40
        arcade.draw_text(
            f"{self._about_info['title']}  {self._about_info['version']}",
            center_x, title_y,
            arcade.color.YELLOW_ORANGE,
            font_size=44,
            font_name=self.font_name,
            anchor_x="center",
            anchor_y="top",
        )

        # 作者信息
        author_y = title_y - 74
        arcade.draw_text(
            f"作者: {self._about_info['author']}",
            center_x - popup_width // 2 + 30, author_y,
            arcade.color.BLACK,
            font_size=30,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="top"
        )

        # 团队标签
        group_y = author_y - 60
        arcade.draw_text(
            "团队:",
            center_x - popup_width // 2 + 40, group_y,
            arcade.color.BLACK,
            font_size=28,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="top"
        )

        # 团队成员
        for i, (name, title) in enumerate(self._about_info["group"]):
            arcade.draw_text(
                f"- {name}（{title}）",
                center_x - popup_width // 2 + 80, group_y - 48 - i * 40,
                arcade.color.DARK_BLUE,
                font_size=26,
                font_name=self.font_name,
                anchor_x="left",
                anchor_y="top"
            )

        # 纯白关闭按钮(圆角16)
        btn_w, btn_h = 140, 56
        btn_x = center_x
        btn_y = center_y - popup_height // 2 + 40
        close_btn_color = arcade.color.LIGHT_GRAY
        self._draw_rounded_rect(btn_x, btn_y, btn_w, btn_h, close_btn_color, radius=16)
        arcade.draw_text(
            "关闭", btn_x, btn_y - 14, arcade.color.BLACK, 28, font_name=self.font_name, anchor_x="center"
        )
        self.close_button_rect = (btn_x - btn_w // 2, btn_y - btn_h // 2, btn_x + btn_w // 2, btn_y + btn_h // 2)

    def on_key_press(self, key, modifiers):
        if self.about_popup:
            if key == arcade.key.ESCAPE or key == arcade.key.ENTER or key == arcade.key.SPACE:
                self.about_popup = False
            return
        if key in (arcade.key.UP, arcade.key.W):
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif key in (arcade.key.ENTER, arcade.key.SPACE):
            self.buttons[self.selected_index]["callback"]()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.about_popup:
            if self.close_button_rect:
                x0, y0, x1, y1 = self.close_button_rect
                if x0 <= x <= x1 and y0 <= y <= y1:
                    self.about_popup = False
            return
        for i, btn in enumerate(self.buttons):
            bx, by = btn["center"]
            if (bx - self.button_width // 2 < x < bx + self.button_width // 2 and
                    by - self.button_height // 2 < y < by + self.button_height // 2):
                self.selected_index = i
                btn["callback"]()

    def show_about(self):
        self.about_popup = True