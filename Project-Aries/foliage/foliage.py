import typing
import arcade
import random

TILE_SCALING:float = 0.5
PLATFORM_HEIGHT:int = int(128 * TILE_SCALING)
SCREEN_WIDTH:int = 1000
SCREEN_HEIGHT:int = 480

FOLIAGE_SCALING:float = 0.07

class Foliage(arcade.Sprite):
    def __init__(self, position:int = 0) -> None:
        super().__init__(filename=r"foliage/Assets/foliage (1).png", scale=FOLIAGE_SCALING)
        self.bottom = PLATFORM_HEIGHT
        self.randomize_all(position)

    def randomize_image(self) -> None:
        """Randomizes the image of the foliage"""
        foliage_path:str = f"foliage/Assets/foliage ({random.randint(1, 26)}).png"
        self.texture = arcade.load_texture(foliage_path)
    
    def randomize_x(self, position:int = 0) -> None:
        """Randomizes the x position of the foliage"""
        self.center_x = random.randint(position, position+SCREEN_WIDTH)
    
    def randomize_all(self, position:int = 0) -> None:
        """Randomizes the image and x position of the foliage"""
        self.randomize_image()
        self.randomize_x(position)
