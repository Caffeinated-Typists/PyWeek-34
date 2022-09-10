import sys, os
import math
import random
import typing
import arcade
from time import time
sys.path.append(os.getcwd() + r"\Project-Aries")
from characters.enemy import Enemy

SCREEN_WIDTH:int = 1000
SCREEN_HEIGHT:int = 480

SPACESHIP_HITPOINTS:int = 500
SPACESHIP_SCALING:float = 1
SPACESHIP_X_POS:int = 19*SCREEN_WIDTH//20
SPACESHIP_INIT_Y_VEL:int = 10

LAYER_ENEMY_BULLETS:str = "Enemy_Bullets"
BULLET_SPEED:int = 5
BULLET_SCALE:float = 0.8
BULLET_PATH:str = "characters/Spaceship/laser.png"
BULLET_MARGIN_X:int = 0
BULLET_MARGIN_Y:int = 0

class SpaceShip(Enemy):

    def __init__(self) -> None:
        """Initialize the class"""
        super().__init__(hitpoints = SPACESHIP_HITPOINTS, scale = SPACESHIP_SCALING)
        self.last_shot = time()
        self.can_shoot:bool = False
        self.center_x = SPACESHIP_X_POS
        self.center_y = SCREEN_HEIGHT
        self.texture:arcade.Texture = arcade.load_texture(f"characters/Spaceship/Ship{random.randint(1, 5)}.png")
        self.death_textures:list[arcade.Texture] = list()
        for itr in range(1, 4):
            self.death_textures.append(arcade.load_texture(f"characters/Spaceship/Ship_damage{itr}.png"))
        self.change_y = -SPACESHIP_INIT_Y_VEL
        self.change_x = 0

    def shoot(self, scene:arcade.scene) -> None:
        """Shoot a bullet from the spaceship"""
        bullet:arcade.Sprite = arcade.Sprite("characters\Spaceship\laser.png", BULLET_SCALE)
        bullet.center_x = self.center_x - BULLET_MARGIN_X
        bullet.center_y = self.center_y - BULLET_MARGIN_Y
        bullet.change_x = -BULLET_SPEED
        scene.add_sprite(LAYER_ENEMY_BULLETS, bullet)
        self.last_shot = time()
        self.can_shoot = False