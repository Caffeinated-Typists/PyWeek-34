import arcade
import typing

class Enemy(arcade.Sprite):

    def __init__(self, scale) -> None:
        """Initialize the enemy class"""
        super().__init__(scale = scale)
        self.hitpoints:int
        self.cur_texture:int = 0
        
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

    def update_bullet_damage(self, damage:int) -> bool:
        """Update the hitpoints of Sprite after being hit by a bullet, returns True if the enemy dies"""
        self.hitpoints = min(self.hitpoints - damage, 0)
        if self.hitpoints == 0:
            #Implement a function to play death animation
            return True
        else:
            return False

    def update_animation(self, delta_time: float):
        """Update the animations upon death"""
        self.cur_texture += 1
        if self.cur_texture >= len(self.textures):
            self.cur_texture = 0
        self.texture = self.textures[self.cur_texture]