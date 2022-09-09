import math
import random
import typing
import arcade

# Constants
UFO_SCALING:float = 1
SCREEN_WIDTH:int = 1000
SCREEN_HEIGHT:int = 480


class UFO(arcade.Sprite):

    def __init__(self, position: int = 0) -> None:
        super().__init__(filename="characters/UFO Sprites/ufo1.png", scale=UFO_SCALING)
        self.randomize_all(position)    

    def randomize_image(self) -> None:
        """Randomizes the image of the cloud"""
        ufo_path = f"characters/UFO Sprites/ufo{random.randint(1, 4)}.png"
        self.texture = arcade.load_texture(ufo_path)
    
    def randomize_x(self, position:int = 0) -> None:
        """Randomizes the x position of the cloud"""
        self.center_x = random.randint(position + SCREEN_WIDTH // 3, position + 2 * SCREEN_WIDTH//3)

    def randomize_y(self) -> None:
        """Randomizes the y position of the cloud"""
        self.center_y = random.randint(2 * (SCREEN_HEIGHT // 3), SCREEN_HEIGHT - 100)

    def randomize_all(self, position:int = 0) -> None:
        """Randomizes the image, x and y position of the cloud"""
        self.randomize_image()
        self.randomize_x(position)
        self.randomize_y()
