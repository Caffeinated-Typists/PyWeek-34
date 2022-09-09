import typing
import arcade
import random

TILE_SCALING:float = 0.5
PLATFORM_HEIGHT:int = int(128 * TILE_SCALING)
OBJ_SCALING:float = 0.4
SCREEN_WIDTH:int = 1000
SCREEN_HEIGHT:int = 480

class EnvObject(arcade.Sprite):
    def __init__(self, position:int = 0) -> None:
        super().__init__(filename=f"env_objects/Assets/cactus{random.randint(1, 5)}.png", scale=OBJ_SCALING)
        self.bottom = PLATFORM_HEIGHT
        self.randomize_all(position)

    def randomize_image(self) -> None:
        """Randomizes the image of the object"""
        cloud_path = f"env_objects/Assets/cactus{random.randint(1, 5)}.png"
        self.texture = arcade.load_texture(cloud_path)
    
    def randomize_x(self, position:int = 0) -> None:
        """Randomizes the x position of the object"""
        self.center_x = random.randint(position, position+SCREEN_WIDTH)    
    
    def randomize_all(self, position:int = 0) -> None:
        """Randomizes the image, and x position of the object"""
        self.randomize_image()
        self.randomize_x(position)
    
    

