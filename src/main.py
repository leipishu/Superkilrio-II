import arcade
import math
from constants import *
from player import Player
from levels.level_manager import LevelManager
from utils.logging_config import logger
from src.ecs.systems.dialogue_system import DialogueSystem


class Superkilrio(arcade.Window):
    def __init__(self):
        self.logger = logger.getChild('GameWindow')
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Core game elements
        self.player = Player()
        self.level_manager = LevelManager()
        self.background = None
        self.held_keys = set()

        # NPC interaction system
        self.dialogue_system = DialogueSystem()
        self.near_npc = None

        # Debug switch
        self.debug_mode = True
        self.font_name = "Microsoft YaHei"

        self.setup()

    def setup(self):
        """Initialize game resources"""
        try:
            self.background = arcade.load_texture(get_asset_path("background.png"))
            if self.debug_mode:
                self.logger.info("Background loaded successfully")
        except Exception as e:
            if self.debug_mode:
                self.logger.error(f"Background loading failed: {str(e)}")

        self.level_manager.load_levels()
        self.level_manager.goto_level(0)
        self.logger.info(f"Current level: {self.level_manager.current_level_num}")
        self.logger.debug(f"Player initial position: ({self.player.center_x}, {self.player.center_y})")

    def on_draw(self):
        """Render the game screen"""
        arcade.start_render()

        # Draw background
        if self.background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                self.background
            )

        # Draw ground
        arcade.draw_line(0, GROUND_Y, SCREEN_WIDTH, GROUND_Y, arcade.color.BLACK, 3)

        # Draw level content
        self.level_manager.draw()

        # Draw player
        self.player.draw()

        # Draw dialogue system
        self.dialogue_system.draw()

        # Debug information
        if self.debug_mode:
            self._draw_debug_info()
            # Draw NPC interaction hint
            if self.near_npc and not self.dialogue_system.is_visible:
                arcade.draw_text(
                    "按E键交互",
                    self.near_npc.center_x,
                    self.near_npc.top + 20,
                    arcade.color.WHITE,
                    16,
                    anchor_x="center"
                )

    def _draw_debug_info(self):
        """Draw debug information"""
        arcade.draw_text(
            f"Level: {self.level_manager.current_level_num}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 20,
            font_name=self.font_name
        )

    def on_update(self, delta_time):
        """Update game logic"""
        self.player.update()
        self.player.update_animation(delta_time)
        self.level_manager.update(delta_time)

        # Check NPC proximity
        self._check_npc_proximity()

        self._apply_physics()

        if self.debug_mode and arcade.key.SPACE in self.held_keys:
            self.logger.debug(f"Player position: ({self.player.center_x:.1f}, {self.player.center_y:.1f})")

    def _check_npc_proximity(self):
        """Check if player is near an NPC"""
        self.near_npc = None
        if self.level_manager.current_level and hasattr(self.level_manager.current_level, 'npcs'):
            for npc in self.level_manager.current_level.npcs:
                # Calculate distance between player and NPC
                distance = math.sqrt(
                    (self.player.center_x - npc.center_x) ** 2 +
                    (self.player.center_y - npc.center_y) ** 2
                )
                if distance <= 100:  # Interaction range
                    self.near_npc = npc
                    break

    def _apply_physics(self):
        """Apply physics effects"""
        self.player.change_y -= GRAVITY
        if self.player.bottom <= GROUND_Y:
            self.player.bottom = GROUND_Y
            self.player.change_y = 0
            self.player.is_on_ground = True
            self.player.remaining_jumps = MAX_EXTRA_JUMPS
        else:
            self.player.is_on_ground = False

    def on_key_press(self, key, modifiers):
        """Keyboard press"""
        self.held_keys.add(key)

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
        elif key == arcade.key.E and self.near_npc:  # NPC interaction
            if not self.dialogue_system.is_visible:
                if hasattr(self.near_npc, 'get_dialogue'):
                    self.dialogue_system.start_dialogue(self.near_npc.get_dialogue())
            else:
                if self.dialogue_system.next_line():
                    self.logger.debug("Dialogue ended")

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