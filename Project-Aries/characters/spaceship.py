import sys, os
import math
import random
import typing
import arcade
sys.path.append(os.getcwd() + r"\Project-Aries")
from characters.enemy import Enemy

SPACESHIP_HITPOINTS:int = 500
SPACESHIP_SCALING:float = 1

class SpaceShip(Enemy):

    def __init__(self) -> None:
        """Initialize the class"""
        super().__init__(hitpoints = SPACESHIP_HITPOINTS, scale = SPACESHIP_SCALING)
        self.set_pos_x()
        self.set_pos_y()
        self.texture = arcade.load_texture(f"characters/Spaceship/enemy{random.randint(1, 5)}.png")

    def on_update(self, delta_time: float = 1 / 60):
        return super().on_update(delta_time)