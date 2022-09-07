import typing
import arcade

PROTAGONIST_SPEED:int = 10
PROTAGONIST_JUMP_SPEED:int = 20

class Protagonist(arcade.Sprite):

    def __init__(self) -> None:
        """Initialize the character"""
        super().__init__(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self.horizontal_vel:int = PROTAGONIST_SPEED
        self.jump_vel:int = PROTAGONIST_JUMP_SPEED
        
    def set_pos_x(self, x:int) -> None:
        """Set the x coordinate of the player"""
        self.center_x = x
    
    def set_pos_left(self, x:int) -> None:
        """Set the left boundary of the player"""
        self.left = x   

    def set_pos_y(self, y:int) -> None:
        """Set the y coordinate of the player"""
        self.center_y = y

    def update_pos_x(self, x:int) -> None:
        """Update the x coordinate of the player"""
        self.center_x += x

    def update_pos_y(self, y:int) -> None:
        """Update the y coordinate of the player"""
        self.center_y += y

    def set_vel_x(self, x:int) -> None:
        """Set the x velocity of the player"""
        self.change_x = x

    def set_vel_y(self, y:int) -> None:
        """Set the y velocity of the player"""
        self.change_y = y

    def update_vel_x(self, x:int) -> None:
        """Update the x velocity of the player"""
        self.change_x += x

    def update_vel_y(self, y:int) -> None:
        """Update the y velocity of the player"""
        self.change_y += y

    def stationary_x(self) -> None:
        """Set x-velocity to 0"""
        self.change_x = 0

    def go_left(self) -> None:
        """Update the speed in x direction to go left"""
        self.set_vel_x(-self.horizontal_vel)

    def go_right(self) -> None:
        """Update the speed in x direction to go right"""
        self.set_vel_x(self.horizontal_vel)

    def jump(self) -> None:
        """Update the y-velocity for jumping"""
        self.update_vel_y(self.jump_vel)