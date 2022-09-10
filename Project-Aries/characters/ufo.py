import sys, os
import math
import random
import typing
import arcade
sys.path.append(os.getcwd() + r"\Project-Aries")
from characters.enemy import Enemy

#FILE PATH
PATH:str = r"characters\UFO Sprites\spritesheet_spaceships.png"

# UFO Constants
UFO_SCALING:float = 1
UFO_HITPOINTS:int = 100

class UFO(Enemy):

    def __init__(self, position: int = 0) -> None:
        super().__init__(hitpoints=UFO_HITPOINTS, scale=UFO_SCALING)
        self.randomize_all(position)    

    def randomize_image(self) -> None:
        """Randomizes the image of the cloud"""
        idx:int = random.randint(0, 4)
        self.texture = arcade.load_texture(f"characters/UFO Sprites/ship_{idx}.png")
        # self.death_textures = self.cur_textures[1]

    def randomize_all(self, position:int = 0) -> None:
        """Randomizes the image, x and y position of the cloud"""
        self.randomize_image()
        self.randomize_x(position)
        self.randomize_y()

    def load_png(self, idx:int) -> list[arcade.Texture, list[arcade.Texture]]:
        """Helper function to load the Sprite"""

        ship:arcade.Texture = arcade.load_texture(f"characters/UFO Sprites/ship_{idx}.png")
        ship_death_textures:list[arcade.Texture] = list()
        ship_death_textures.append(arcade.load_texture(f"characters/UFO Sprites/ship_damage_{idx}.png"))
        ship_death_textures.append(arcade.load_texture(f"characters/UFO Sprites/ship_damage_{idx}.png"))
        
        return list[ship, ship_death_textures]
