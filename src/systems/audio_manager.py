# src/systems/audio_manager.py
import arcade
import os
import gc
from src.constants import get_asset_path
from src.utils.logging_config import logger

class AudioManager:
    """全局音频管理器 - 统一管理所有音频资源"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.sounds = {}
        self._cleaned_up = False
        self._load_sounds()
        self._initialized = True

    def _load_sounds(self):
        """载入所有音频文件"""
        try:
            hit_sound_path = get_asset_path("snd/hit.mp3")
            if os.path.exists(hit_sound_path):
                self.sounds['hit'] = arcade.load_sound(hit_sound_path)
                logger.debug("Hit sound loaded successfully")
            else:
                logger.warning(f"Hit sound file not found: {hit_sound_path}")
                self.sounds['hit'] = None
        except Exception as e:
            logger.error(f"Failed to load sounds: {e}")
            self.sounds['hit'] = None

    def play_sound(self, sound_name, volume=0.2):
        """播放音频"""
        if self._cleaned_up:
            return
        sound = self.sounds.get(sound_name)
        if sound:
            try:
                arcade.play_sound(sound, volume=volume)
            except Exception as e:
                logger.warning(f"Failed to play sound {sound_name}: {e}")

    def cleanup(self):
        """清理所有音频资源"""
        if self._cleaned_up:
            return
        try:
            for k in self.sounds:
                self.sounds[k] = None
            self.sounds.clear()
            self._cleaned_up = True
            gc.collect()
            logger.info("AudioManager cleanup completed successfully")
        except Exception as e:
            logger.error(f"Error during AudioManager cleanup: {e}")
            self._cleaned_up = True

    def __del__(self):
        try:
            self.cleanup()
        except Exception:
            pass

# 全局单例
audio_manager = AudioManager()