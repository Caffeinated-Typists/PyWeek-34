import typing
import arcade
import random

TILE_SCALING:float = 0.5
PLATFORM_HEIGHT:int = int(128 * TILE_SCALING)
SCREEN_WIDTH:int = 1000
SCREEN_HEIGHT:int = 480

FOLIAGE_SCALING:float = 0.3

class Foliage(arcade.Sprite):
    def __init__(self, position:int = 0) -> None:
        super().__init__(scale=FOLIAGE_SCALING)
        self.bottom = PLATFORM_HEIGHT
        self.randomize_all(position)

    def randomize_image(self) -> None:
        """Randomizes the image of the foliage"""
        cloud_path = f"characters/Assets/foliage ({random.randint(1, 26)}).png"
        self.texture = arcade.load_texture(cloud_path)
    
    def randomize_x(self, position:int = 0) -> None:
        """Randomizes the x position of the foliage"""
        self.center_x = random.randint(position + SCREEN_WIDTH // 3, position + 2 * SCREEN_WIDTH//3)
    
    def randomize_all(self, position:int = 0) -> None:
        """Randomizes the image and x position of the foliage"""
        self.randomize_image()
        self.randomize_x(position)
