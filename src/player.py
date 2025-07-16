import arcade
from constants import *
from PIL.Image import FLIP_LEFT_RIGHT
from utils.logging_config import logger
import time


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.logger = logger.getChild('Player')

        # 加载纹理
        assets_dir = get_asset_path("player")
        try:
            self.run_frames = [arcade.load_texture(f"{assets_dir}/run_{i}.png") for i in range(1, 7)]
            self.stand_texture = arcade.load_texture(f"{assets_dir}/stand.png")
            self.jump_texture = arcade.load_texture(f"{assets_dir}/jump.png")
            self.attack_textures = [
                arcade.load_texture(f"{assets_dir}/attack_1.png"),
                arcade.load_texture(f"{assets_dir}/attack_2.png")
            ]
            self.logger.debug("Player textures loaded successfully")
        except Exception as e:
            self.logger.error(f"Texture loading failed: {str(e)}")
            raise

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

        # 跳跃相关
        self.remaining_jumps = 1
        self.is_on_ground = True

        # 攻击系统
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_frame = 0
        self.attack_timer = 0
        self.last_attack_time = 0
        self.has_dealt_damage = False  # 新增：标记是否已造成伤害

    def update_animation(self, delta_time):
        """更新动画状态"""
        # 跳跃状态检测
        self.is_on_ground = (self.bottom <= GROUND_Y and self.change_y == 0)
        if self.is_on_ground:
            self.remaining_jumps = 1

        # 攻击动画优先
        if self.is_attacking:
            self.attack_timer += delta_time
            frame_duration = ATTACK_ANIMATION_SPEED

            # 两帧攻击动画
            if self.attack_timer < frame_duration:
                self.attack_frame = 0
            elif self.attack_timer < frame_duration * 2:
                self.attack_frame = 1
            else:
                # 攻击结束
                self.is_attacking = False
                self.attack_timer = 0
                self.attack_frame = 0
                self.has_dealt_damage = False  # 重置伤害标记

            self.texture = self.attack_textures[self.attack_frame]
            if not self.facing_right:
                flipped = self.texture.image.transpose(FLIP_LEFT_RIGHT)
                self.texture = arcade.Texture(f"{self.texture.name}_flipped", flipped)
            return

        # 原有动画逻辑
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

    def try_attack(self):
        """尝试进行攻击"""
        current_time = time.time()
        if current_time - self.last_attack_time >= ATTACK_COOLDOWN:
            self.is_attacking = True
            self.attack_timer = 0
            self.last_attack_time = current_time
            self.has_dealt_damage = False  # 重置伤害标记
            return True
        return False

    def get_attack_hitbox(self):
        """获取攻击判定框"""
        if not self.is_attacking:
            return None

        # 根据面向方向调整攻击范围
        direction = 1 if self.facing_right else -1
        hitbox_x = self.center_x + (direction * ATTACK_RANGE / 2)
        hitbox_y = self.center_y

        # 攻击判定框
        return {
            'left': hitbox_x - ATTACK_RANGE / 2,
            'right': hitbox_x + ATTACK_RANGE / 2,
            'bottom': hitbox_y - 40,
            'top': hitbox_y + 40
        }