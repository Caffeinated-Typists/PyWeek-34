import typing
import arcade
import random

CLOUD_SCALING:float = 0.3
SCREEN_WIDTH:int = 1000
SCREEN_HEIGHT:int = 480

class Cloud(arcade.Sprite):
    def __init__(self, position:int = 0) -> None:
        super().__init__(filename=f"characters/Clouds/cloud{random.randint(1, 4)}.png", scale=CLOUD_SCALING)

    def randomize_image(self) -> None:
        cloud_path = f"characters/Clouds/cloud{random.randint(1, 4)}.png"
        self.texture = arcade.load_texture(cloud_path)
    
    def randomize_x(self, position:int = 0) -> None:
        self.center_x = random.randint(position + SCREEN_WIDTH // 3, position + 2 * SCREEN_WIDTH//3)
    
    def randomize_y(self) -> None:
        self.center_y = random.randint(2 * (SCREEN_HEIGHT // 3), SCREEN_HEIGHT - 100)
    
    def randomize_all(self, position:int = 0) -> None:
        self.randomize_image()
        self.randomize_x(position)
        self.randomize_y()

    
    

