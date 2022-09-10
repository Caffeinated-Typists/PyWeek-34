import arcade
import typing
import random

#SCREEN CONSTANTS
SCREEN_WIDTH:int = 1000
SCREEN_HEIGHT:int = 480

#Layer names
LAYER_DEATH:str = "Death"

class Enemy(arcade.Sprite):

    def __init__(self, hitpoints:int, scale:int = 1) -> None:
        """Initialize the enemy class"""
        super().__init__(scale = scale)
        self.hitpoints:int = hitpoints
        self.cur_texture:int = 0
        self.death_textures:list[arcade.Texture] = None
        
    def set_pos_x(self, x:int) -> None:
        """Set x-position of Sprite"""
        self.center_x = x

    def set_pos_y(self, y:int) -> None:
        """Set y-position of Sprite"""
        self.center_x = y

    def set_pos(self, x:int, y:int) -> None:
        """Set position of Sprite"""
        self.set_pos_x(x)
        self.set_pos_y(y)

    def set_vel_x(self, x:int) -> None:
        """Set the x-velocity of Sprite"""
        self.change_x = x

    def set_vel_y(self, y:int) -> None:
        """Set the y-velocity of Sprite"""
        self.change_x = y

    def set_vel(self, x:int, y:int) -> None:
        """Set the velocity of Sprite"""
        self.set_vel_x(x)
        self.set_vel_y(y)

    def randomize_x(self, position:int = 0) -> None:
        """Randomizes the x position of the cloud"""
        self.center_x = random.randint(position + SCREEN_WIDTH // 3, position + 2 * SCREEN_WIDTH//3)

    def randomize_y(self) -> None:
        """Randomizes the y position of the cloud"""
        self.center_y = random.randint(2 * (SCREEN_HEIGHT // 3), SCREEN_HEIGHT - 100)

    def update_bullet_damage(self, damage:int) -> bool:
        """Update the hitpoints of Sprite after being hit by a bullet, returns True if the enemy dies"""
        self.hitpoints = max(self.hitpoints - damage, 0)
        if self.hitpoints == 0:
            return True
        else:
            return False
    
    def play_dead_animation(self, scene:arcade.scene) -> None:
        """Add a Sprite to play the death animation to scene"""
        death_sprite:Death_Sprite = Death_Sprite(self.death_textures)
        death_sprite.center_x = self.center_x
        death_sprite.center_y = self.center_y
        scene.add_sprite(LAYER_DEATH, death_sprite)

    def update_animation(self, delta_time: float):
        """Update the animations"""
        self.cur_texture += 1
        if self.cur_texture >= len(self.textures):
            self.cur_texture = 0
        self.texture = self.textures[self.cur_texture]


class Death_Sprite(arcade.Sprite):

    def __init__(self, death_animations:list[arcade.Texture], scale:float = 1, dont_delete:bool = False):
        """Initialize the class"""
        super().__init__(scale = scale)
        self.textures:list[arcade.Texture] = death_animations
        self.cur_texture_index:int = 0
        self.delete = not dont_delete

    def update_animation(self, delta_time: float):
        if self.cur_texture_index < len(self.textures):
            self.texture = self.textures[self.cur_texture_index]
        else:
            if not self.delete:
                self.texture = self.textures[-1]
            else:
                self.remove_from_sprite_lists()

        self.cur_texture_index += 1