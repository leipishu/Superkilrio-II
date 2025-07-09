# src/systems/physics_system.py
from src.constants import *

class PhysicsSystem:
    def __init__(self):
        pass

    def apply_physics(self, player):
        """应用物理效果"""
        player.change_y -= GRAVITY
        if player.bottom <= GROUND_Y:
            player.bottom = GROUND_Y
            player.change_y = 0
            player.is_on_ground = True
            player.remaining_jumps = MAX_EXTRA_JUMPS
        else:
            player.is_on_ground = False