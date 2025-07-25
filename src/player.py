import arcade
from constants import *
from PIL.Image import FLIP_LEFT_RIGHT
from utils.logging_config import logger
from src.systems.particle_system import ParticleSystem
from src.items.dropped_item import DroppedItem
import time


class Player(arcade.Sprite):
    def __init__(self, game=None):
        super().__init__()
        self.logger = logger.getChild('Player')
        self.particle_system = ParticleSystem()
        self.inventory = [None] * INVENTORY_SLOT_COUNT  # 物品栏数组
        self.selected_slot = 0  # 当前选中的格子索引
        self.equipped_weapon = None  # 当前装备的武器
        self.weapon_attack_textures = {}  # 武器攻击动画缓存

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

        # 生命值
        self.max_health = PLAYER_MAX_HEALTH
        self.health = PLAYER_MAX_HEALTH
        self.is_dead = False

    def update_animation(self, delta_time):
        """更新动画状态，支持武器动画"""
        if self.is_attacking:
            self.attack_timer += delta_time
            frame_duration = ATTACK_ANIMATION_SPEED

            if self.equipped_weapon:
                frame_duration /= self.equipped_weapon.attack_speed

            if self.attack_timer < frame_duration:
                self.attack_frame = 0
            elif self.attack_timer < frame_duration * 2:
                self.attack_frame = 1
            else:
                self.is_attacking = False
                self.attack_timer = 0
                self.attack_frame = 0
                self.has_dealt_damage = False

            # 使用武器动画或默认动画
            textures = self.weapon_attack_textures.get(
                self.equipped_weapon.item_id if self.equipped_weapon else None,
                self.attack_textures
            )
            self.texture = textures[self.attack_frame]

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
        """尝试进行攻击，使用武器属性"""
        current_time = time.time()
        cooldown = ATTACK_COOLDOWN
        if self.equipped_weapon:
            cooldown /= self.equipped_weapon.attack_speed

        if current_time - self.last_attack_time >= cooldown:
            self.is_attacking = True
            self.attack_timer = 0
            self.last_attack_time = current_time
            self.has_dealt_damage = False
            return True
        return False

    def take_damage(self, amount):
        """玩家受伤"""
        if self.is_dead:
            return
        self.health -= amount
        self.particle_system.create_hurt_effect(self.center_x, self.center_y)
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.logger.info('Player died!')

    def get_attack_hitbox(self):
        """获取攻击判定框，使用武器范围"""
        if not self.is_attacking:
            return None

        attack_range = ATTACK_RANGE
        if self.equipped_weapon:
            attack_range = self.equipped_weapon.attack_range

        direction = 1 if self.facing_right else -1
        hitbox_x = self.center_x + (direction * attack_range / 2)

        return {
            'left': hitbox_x - attack_range / 2,
            'right': hitbox_x + attack_range / 2,
            'bottom': self.center_y - 40,
            'top': self.center_y + 40
        }

    def equip_weapon(self, weapon):
        """装备武器"""
        self.equipped_weapon = weapon
        self.logger.info(f"Equipped weapon: {weapon.name}")

        # 预加载武器攻击动画
        if weapon.item_id not in self.weapon_attack_textures:
            try:
                assets_dir = get_asset_path(f"player/{weapon.item_id}")
                self.weapon_attack_textures[weapon.item_id] = [
                    arcade.load_texture(f"{assets_dir}/attack_1.png"),
                    arcade.load_texture(f"{assets_dir}/attack_2.png")
                ]
                self.logger.debug(f"Loaded weapon textures for {weapon.item_id}")
            except Exception as e:
                self.logger.warning(f"Failed to load weapon textures: {str(e)}")
                # 使用默认攻击动画作为后备
                self.weapon_attack_textures[weapon.item_id] = self.attack_textures

    def unequip_weapon(self):
        """取消装备当前武器"""
        if self.equipped_weapon:
            weapon_name = self.equipped_weapon.name
            self.equipped_weapon = None
            self.logger.info(f"Unequipped weapon: {weapon_name}")
            return True
        return False

    def drop_item(self, slot):
        if not 0 <= slot < len(self.inventory) or not self.inventory[slot]:
            return None

        # 如果丢弃的是已装备的武器，先解除装备
        if self.equipped_weapon and self.inventory[slot] == self.equipped_weapon:
            self.unequip_weapon()

        # 创建掉落物
        item = self.inventory[slot]
        dropped_item = DroppedItem(
            item=item,
            x=self.center_x,
            y=self.center_y + 50  # 从玩家头顶上方掉落
        )

        # 从物品栏移除
        self.inventory[slot] = None

        return dropped_item