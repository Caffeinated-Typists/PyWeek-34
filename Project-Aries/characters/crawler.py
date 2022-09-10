import sys, os
import math
import random
import typing
import arcade
sys.path.append(os.getcwd() + r"\Project-Aries")
from characters.enemy import Enemy

CRAWLER_SCALING:float = 0.15
CRAWLER_HITPOINTS:int = 500
CRAWLER_SPEED_RATIO = 1.33

class Crawler(Enemy):

    def __init__(self, position:int, game_speed:int) -> None:
        """Initialize the position"""
        super().__init__(hitpoints=CRAWLER_HITPOINTS, scale=CRAWLER_SCALING)
        
        self.randomize_x(position)   #FIX THIS
        self.change_x:float = -CRAWLER_SPEED_RATIO*game_speed
        self.load_animations()
        self.texture = self.textures[0]
        self.bottom:int = 64

    def load_animations(self) -> None:
        """Loads the png for animating the character"""
        for itr in range(21):
            self.textures.append(arcade.load_texture(f"characters/Crawler/skeleton-walking_{itr}.png"))

    