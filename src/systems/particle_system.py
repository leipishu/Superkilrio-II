# src/systems/particle_system.py
import arcade
import random
import gc
from src.constants import *
from src.utils.logging_config import logger
from src.systems.audio_manager import audio_manager
import os


class SingleHitParticle:
    """单个击中效果粒子"""

    def __init__(self, x, y, texture):
        self.sprite = arcade.Sprite()
        self.sprite.texture = texture
        self.sprite.scale = 0.3  # 减小大小
        self.sprite.center_x = x
        self.sprite.center_y = y

        # 轻微浮动效果
        self.initial_y = y
        self.float_offset = random.uniform(-5, 5)
        self.lifetime = 0.4

    def update(self, delta_time):
        """更新粒子状态"""
        self.lifetime -= delta_time

        # 轻微上浮效果
        progress = 1 - (self.lifetime / 0.4)
        self.sprite.center_y = self.initial_y + (progress * 20) + self.float_offset

        # 淡出效果
        alpha = max(0, int(255 * (self.lifetime / 0.4)))
        self.sprite.alpha = alpha

        return self.lifetime > 0


class ParticleSystem:
    """单粒子系统管理器 - 使用全局音频管理器"""

    def __init__(self):
        self.particle = None
        self.hit_texture = None
        self.kill_texture = None
        self.kill_sprite = None
        self.kill_timer = 0
        self._cleaned_up = False  # 防止重复清理
        self.load_texture()

    def load_texture(self):
        """加载击中效果纹理"""
        try:
            texture_path = get_asset_path("effects/hit.png")
            self.hit_texture = arcade.load_texture(texture_path)
            # 加载 kill.png
            kill_path = get_asset_path("effects/kill.png")
            self.kill_texture = arcade.load_texture(kill_path)
            logger.debug("Hit texture loaded")
        except Exception as e:
            logger.warning(f"Failed to load hit texture: {e}")
            # 创建备用纹理
            self.hit_texture = arcade.Texture.create_filled(
                "white_square", (8, 8), arcade.color.YELLOW
            )
            self.kill_texture = arcade.Texture.create_filled(
                "kill", (32, 32), arcade.color.RED
            )

    def create_hit_effect(self, x, y, is_kill=False):
        """创建单个击中效果"""
        self.particle = SingleHitParticle(x, y, self.hit_texture)
        # 使用全局音频管理器播放音效
        if not self._cleaned_up:
            audio_manager.play_sound('hit', volume=0.2)
        if is_kill:
            self.kill_sprite = arcade.Sprite(texture=self.kill_texture, scale=0.4)
            self.kill_sprite.center_x = x
            self.kill_sprite.center_y = y + 40  # 敌人头顶
            self.kill_timer = 0.5 # 显示0.5秒

    def update(self, delta_time):
        """更新单个粒子"""
        if self.particle:
            if not self.particle.update(delta_time):
                self.particle = None
        if self.kill_sprite:
            self.kill_timer -= delta_time
            if self.kill_timer <= 0:
                self.kill_sprite = None

    def draw(self):
        """绘制单个粒子"""
        if self.particle:
            self.particle.sprite.draw()
        if self.kill_sprite:
            self.kill_sprite.draw()

    def cleanup(self):
        """清理粒子系统资源"""
        if self._cleaned_up:
            return  # 防止重复清理
            
        try:
            # 清理粒子资源
            self.particle = None
            self.kill_sprite = None
            
            # 标记已清理
            self._cleaned_up = True
            logger.info("Particle system resources cleaned up successfully")
            
        except Exception as e:
            logger.error(f"Error during particle system cleanup: {e}")
            self._cleaned_up = True

    def __del__(self):
        """确保资源被清理 - 备用方案"""
        if not self._cleaned_up:
            try:
                self.cleanup()
            except:
                pass  # 在析构函数中忽略所有错误