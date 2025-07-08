import arcade
from constants import *
from player import Player
from levels.level_manager import LevelManager


class Superkilrio(arcade.Window):
    def __init__(self):
        """初始化游戏窗口"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # 游戏核心元素
        self.player = Player()
        self.level_manager = LevelManager()
        self.background = None
        self.held_keys = set()  # 新增：追踪按下的键

        # 调试开关
        self.debug_mode = True

        # 字体设置
        self.font_name = "Microsoft YaHei"  # 新增：微软雅黑字体
        self.setup()

    def setup(self):
        """初始化游戏资源"""
        # 加载背景
        try:
            self.background = arcade.load_texture(get_asset_path("background.png"))
            if self.debug_mode:
                print("✅ 背景加载成功")
        except Exception as e:
            if self.debug_mode:
                print(f"⚠️ 背景加载失败: {str(e)}")

        # 初始化关卡系统
        self.level_manager.load_levels()
        self.level_manager.goto_level(0)  # 强制从第0关开始

    def on_draw(self):
        """渲染游戏画面"""
        arcade.start_render()

        # 1. 绘制背景
        if self.background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                self.background
            )

        # 2. 绘制地面系统
        arcade.draw_line(0, GROUND_Y, SCREEN_WIDTH, GROUND_Y,
                         arcade.color.BLACK, 3)

        # 3. 绘制关卡内容
        self.level_manager.draw()

        # 4. 绘制玩家
        self.player.draw()

        # 5. 调试信息
        if self.debug_mode:
            self._draw_debug_info()

    def _draw_debug_info(self):
        """绘制调试信息"""
        # 移除玩家头顶文字显示

        # 关卡信息（使用微软雅黑字体）
        arcade.draw_text(
            f"关卡: {self.level_manager.current_level_num}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 20,
            font_name=self.font_name  # 使用指定字体
        )

    def on_update(self, delta_time):
        """游戏逻辑更新"""
        # 更新玩家
        self.player.update()
        self.player.update_animation(delta_time)

        # 更新关卡
        self.level_manager.update(delta_time)

        # 物理系统
        self._apply_physics()

        # 调试输出
        if self.debug_mode and arcade.key.SPACE in self.held_keys:
            print(f"玩家坐标: ({self.player.center_x:.1f}, {self.player.center_y:.1f})")

    def _apply_physics(self):
        """物理效果"""
        self.player.change_y -= GRAVITY

        # 地面碰撞
        if self.player.bottom <= GROUND_Y:
            self.player.bottom = GROUND_Y
            self.player.change_y = 0
            self.player.is_on_ground = True
            self.player.remaining_jumps = MAX_EXTRA_JUMPS
        else:
            self.player.is_on_ground = False

    def on_key_press(self, key, modifiers):
        """键盘按下"""
        self.held_keys.add(key)  # 记录按下的键

        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED
            self.player.facing_right = False
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED
            self.player.facing_right = True
        elif key == arcade.key.UP:
            if self.player.is_on_ground or self.player.remaining_jumps > 0:
                self.player.change_y = PLAYER_JUMP_SPEED
                if not self.player.is_on_ground:
                    self.player.remaining_jumps -= 1
        elif key == arcade.key.SPACE:
            if self.level_manager.current_level.is_completed:
                self.level_manager.next_level()
        elif key == arcade.key.F3:
            self.debug_mode = not self.debug_mode

    def on_key_release(self, key, modifiers):
        """键盘释放"""
        if key in self.held_keys:
            self.held_keys.remove(key)

        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0


def main():
    """游戏入口"""
    window = Superkilrio()
    arcade.run()


if __name__ == "__main__":
    main()