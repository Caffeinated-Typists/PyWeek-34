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
UFO_HITPOINTS:int = 500

class UFO(Enemy):

    def __init__(self, position: int = 0) -> None:
        super().__init__(hitpoints=UFO_HITPOINTS, scale=UFO_SCALING)
        self.possible_textures = self.load_png()
        self.randomize_all(position)    

    def randomize_image(self) -> None:
        """Randomizes the image of the cloud"""
        ufo_path = f"characters/UFO Sprites/ufo{random.randint(1, 4)}.png"
        self.texture = arcade.load_texture(ufo_path)

    def randomize_all(self, position:int = 0) -> None:
        """Randomizes the image, x and y position of the cloud"""
        self.randomize_image()
        self.randomize_x(position)
        self.randomize_y()

    def load_png(self) -> list[arcade.Texture]:
        """Helper function to load all the """
