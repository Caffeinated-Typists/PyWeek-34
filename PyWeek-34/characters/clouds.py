import typing
import arcade
import random

CLOUD_SCALING:float = 0.3
SCREEN_WIDTH:int = 1000
SCREEN_HEIGHT:int = 480

class Cloud(arcade.Sprite):
    def __init__(self, position:int = 0) -> None:
        super().__init__(filename=f"characters/Clouds/cloud{random.randint(1, 4)}.png", scale=CLOUD_SCALING)
        self.center_x = random.randint(position + SCREEN_WIDTH // 3, position +  2 * SCREEN_WIDTH//3)
        self.center_y = random.randint(2 * (SCREEN_HEIGHT // 3), int(5*SCREEN_HEIGHT/7))
    

    
    

