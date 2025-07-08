import arcade
from constants import *
from PIL.Image import FLIP_LEFT_RIGHT


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # 加载纹理
        assets_dir = get_asset_path("player")
        self.run_frames = [arcade.load_texture(f"{assets_dir}/run_{i}.png") for i in range(1, 7)]
        self.stand_texture = arcade.load_texture(f"{assets_dir}/stand.png")
        self.jump_texture = arcade.load_texture(f"{assets_dir}/jump.png")

        # 初始化状态
        self.texture = self.stand_texture
        self.scale = PLAYER_SCALE
        self.center_x, self.center_y = 100, GROUND_HEIGHT
        self.facing_right = True
        self.extra_jumps = MAX_EXTRA_JUMPS
        self.was_on_ground = True

        # 动画控制
        self.cur_frame = 0
        self.time_since_last_frame = 0
        self.frames_per_texture = 5

        self.remaining_jumps = 1  # 可额外跳跃次数
        self.is_on_ground = True

    def update_animation(self, delta_time):
        # 跳跃状态检测
        self.is_on_ground = (self.bottom <= GROUND_Y and self.change_y == 0)
        if self.is_on_ground:
            self.remaining_jumps = 1  # 落地重置跳跃次数

        # 原有动画逻辑...
        if self.change_y > 0:
            self.texture = self.jump_texture
        elif self.change_x == 0:
            self.texture = self.stand_texture
        else:
            self.time_since_last_frame += delta_time * 60
            if self.time_since_last_frame >= self.frames_per_texture:
                self.time_since_last_frame = 0
                self.cur_frame = (self.cur_frame + 1) % len(self.run_frames)
                texture = self.run_frames[self.cur_frame]
                if not self.facing_right:
                    flipped = texture.image.transpose(FLIP_LEFT_RIGHT)
                    self.texture = arcade.Texture(f"{texture.name}_flipped", flipped)
                else:
                    self.texture = texture