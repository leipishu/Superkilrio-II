import arcade
from constants import *
from player import Player
from levels.level_manager import LevelManager
from utils.logging_config import logger


class Superkilrio(arcade.Window):
    def __init__(self):
        self.logger = logger.getChild('GameWindow')  # Child logger
        """Initialize the game window"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Core game elements
        self.player = Player()
        self.level_manager = LevelManager()
        self.background = None
        self.held_keys = set()  # New: Track pressed keys

        # Debug switch
        self.debug_mode = True

        # Font settings
        self.font_name = "Microsoft YaHei"  # New: Microsoft YaHei font
        self.setup()

    def setup(self):
        """Initialize game resources"""
        # Load background
        try:
            self.background = arcade.load_texture(get_asset_path("background.png"))
            if self.debug_mode:
                self.logger.info("Background loaded successfully")
        except Exception as e:
            if self.debug_mode:
                self.logger.error(f"Background loading failed: {str(e)}")

        # Initialize level system
        self.level_manager.load_levels()
        self.level_manager.goto_level(0)
        self.logger.info(f"Current level: {self.level_manager.current_level_num}")
        self.logger.debug(f"Player initial position: ({self.player.center_x}, {self.player.center_y})")

    def on_draw(self):
        """Render the game screen"""
        arcade.start_render()

        # 1. Draw background
        if self.background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                self.background
            )

        # 2. Draw ground system
        arcade.draw_line(0, GROUND_Y, SCREEN_WIDTH, GROUND_Y,
                         arcade.color.BLACK, 3)

        # 3. Draw level content
        self.level_manager.draw()

        # 4. Draw player
        self.player.draw()

        # 5. Debug information
        if self.debug_mode:
            self._draw_debug_info()

    def _draw_debug_info(self):
        """Draw debug information"""
        # Remove player头顶 text display

        # Level information (using Microsoft YaHei font)
        arcade.draw_text(
            f"Level: {self.level_manager.current_level_num}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 20,
            font_name=self.font_name  # Use specified font
        )

    def on_update(self, delta_time):
        """Update game logic"""
        # Update player
        self.player.update()
        self.player.update_animation(delta_time)

        # Update level
        self.level_manager.update(delta_time)

        # Physics system
        self._apply_physics()

        # Debug output
        if self.debug_mode and arcade.key.SPACE in self.held_keys:
            self.logger.debug(f"Player position: ({self.player.center_x:.1f}, {self.player.center_y:.1f})")

    def _apply_physics(self):
        """Apply physics effects"""
        self.player.change_y -= GRAVITY

        # Ground collision
        if self.player.bottom <= GROUND_Y:
            self.player.bottom = GROUND_Y
            self.player.change_y = 0
            self.player.is_on_ground = True
            self.player.remaining_jumps = MAX_EXTRA_JUMPS
        else:
            self.player.is_on_ground = False

    def on_key_press(self, key, modifiers):
        """Keyboard press"""
        self.held_keys.add(key)  # Record pressed key

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
        """Keyboard release"""
        if key in self.held_keys:
            self.held_keys.remove(key)

        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0


def main():
    """Game entry point"""
    window = Superkilrio()
    arcade.run()


if __name__ == "__main__":
    main()
