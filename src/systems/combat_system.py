# src/systems/combat_system.py (完整修复版)
import arcade
from src.constants import *
from src.utils.logging_config import logger
from src.systems.particle_system import ParticleSystem
import math


class CombatSystem:
    """战斗系统 - 处理玩家攻击和敌人受伤"""

    def __init__(self, game_controller):
        self.game = game_controller
        self.logger = logger.getChild('CombatSystem')
        self.particle_system = ParticleSystem()

    def find_closest_enemy(self, player, enemies):
        """找到攻击范围内最近的敌人"""
        attack_hitbox = player.get_attack_hitbox()
        if not attack_hitbox or not enemies:
            return None

        closest_enemy = None
        min_distance = float('inf')

        for enemy in enemies:
            if self.check_collision(attack_hitbox, enemy):
                enemy_center_x = (enemy.left + enemy.right) / 2
                enemy_center_y = (enemy.bottom + enemy.top) / 2
                player_center_x = (attack_hitbox['left'] + attack_hitbox['right']) / 2
                player_center_y = (attack_hitbox['bottom'] + attack_hitbox['top']) / 2

                distance = math.sqrt(
                    (enemy_center_x - player_center_x) ** 2 +
                    (enemy_center_y - player_center_y) ** 2
                )

                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy

        return closest_enemy

    def check_collision(self, hitbox, enemy):
        """检查攻击判定框与敌人是否碰撞"""
        return (hitbox['left'] < enemy.right and
                hitbox['right'] > enemy.left and
                hitbox['bottom'] < enemy.top and
                hitbox['top'] > enemy.bottom)

    def apply_damage(self, enemy, damage, hit_x, hit_y):
        """对敌人造成伤害并添加粒子效果"""
        if hasattr(enemy, 'health'):
            enemy.health -= damage
            self.logger.debug(f"Enemy took {damage} damage, remaining health: {enemy.health}")

            # 创建击中粒子效果
            self.particle_system.create_hit_effect(hit_x, hit_y)

            if enemy.health <= 0:
                self.destroy_enemy(enemy)
                return True
        return False

    def destroy_enemy(self, enemy):
        """销毁敌人并添加击杀提示"""
        self.particle_system.create_hit_effect(enemy.center_x, enemy.center_y, is_kill=True)
        enemy.kill()

    def get_entity_name(self, entity):
        """智能获取实体名称"""
        # 1. 优先检查是否有name属性
        if hasattr(entity, 'name') and entity.name:
            return entity.name

        # 2. 检查类名
        class_name = entity.__class__.__name__

        # 3. 根据类名映射友好名称
        name_map = {
            'Level1Grunt': '一级步兵',
            'Level2Grunt': '二级步兵',
            'BossEnemy': '首领',
            'TrainerNPC': '教官',
        }

        if class_name in name_map:
            return name_map[class_name]

        # 4. 简化类名（去掉常见后缀）
        simplified = class_name.replace('Enemy', '').replace('NPC', '')
        if simplified != class_name:
            return simplified

        # 5. 默认处理
        return class_name

    def update(self, delta_time):
        """更新战斗系统和粒子效果"""
        # 更新粒子
        self.particle_system.update(delta_time)
        # 更新击杀提示

        # 检查玩家攻击
        if (self.game.player.is_attacking and
                self.game.player.attack_frame == 1 and
                self.game.level_manager.current_level):

            enemies = self.game.level_manager.current_level.enemies
            target_enemy = self.find_closest_enemy(self.game.player, enemies)

            if target_enemy and not self.game.player.has_dealt_damage:
                # 计算击中位置（敌人中心）
                hit_x = target_enemy.center_x
                hit_y = target_enemy.center_y

                # 修复：添加缺失的hit_x和hit_y参数
                self.apply_damage(target_enemy, ATTACK_DAMAGE, hit_x, hit_y)
                self.game.player.has_dealt_damage = True

        # 重置伤害标记
        if not self.game.player.is_attacking:
            self.game.player.has_dealt_damage = False