import typing
import arcade

PROTAGONIST_SCALING:float = 0.22
PROTAGONIST_SPEED:int = 10
PROTAGONIST_JUMP_SPEED:int = 20

#Constants for getting Images from Sprite List
IMAGE_PIXEL_HEIGHT:int = 599
IMAGE_PIXEL_WIDTH:int = 692

class Protagonist(arcade.Sprite):

    def __init__(self) -> None:
        """Initialize the character"""
        super().__init__(scale = PROTAGONIST_SCALING)
        self.idle_texture:arcade.Texture = arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_standing_idle.png", x = 0, y = 0, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) 
        self.flying_textures:list[arcade.Texture] = [arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_flying_no_movement.png", x = i%5 * IMAGE_PIXEL_WIDTH, y = i//5 * IMAGE_PIXEL_HEIGHT, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) for i in range(10)]
        self.running_textures:list[arcade.Texture] = [arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_standing_run.png", x = i%5 * IMAGE_PIXEL_WIDTH, y = i//5 * IMAGE_PIXEL_HEIGHT, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) for i in range(15)]
        self.walking_textures:list[arcade.Texture] = [arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_standing_walk.png", x = i%5 * IMAGE_PIXEL_WIDTH, y = i//5 * IMAGE_PIXEL_HEIGHT, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) for i in range(15)]
        self.jumping_textures:list[arcade.Texture] = [arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_standing_jump.png", x = i%5 * IMAGE_PIXEL_WIDTH, y = i//5 * IMAGE_PIXEL_HEIGHT, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) for i in range(10)]
        self.texture:arcade.Texture = self.idle_texture

        self.is_flying:bool = False
        self.is_jumping:bool = False
        self.is_running:bool = False
        self.cur_texture:int = 0

        self.horizontal_vel:int = PROTAGONIST_SPEED
        self.jump_vel:int = PROTAGONIST_JUMP_SPEED
        self.set_hit_box([[33, -180], [33, -270]])
        
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
        self.is_jumping = True

    def update_animation(self, delta_time: float) -> None:
        """Update the animation of the Protagonist at every call"""

        if self.change_y == 0:
            self.is_jumping = False

        if self.is_flying:          #If the Protagonist has Jetpack
            self.cur_texture += 1
            if self.cur_texture >= len(self.flying_textures):
                self.cur_texture = 0
            self.texture = self.flying_textures[self.cur_texture]
        elif self.is_jumping:     #If the Protagonist is jumping
                self.cur_texture += 1
                if self.cur_texture >= len(self.jumping_textures):
                    self.cur_texture = 0
                self.texture = self.jumping_textures[self.cur_texture]
        elif self.is_running:   #If the Protagonist is running
            self.cur_texture += 1
            if self.cur_texture >= len(self.running_textures):
                self.cur_texture = 0
            self.texture = self.running_textures[self.cur_texture]
        else:                   #If the Protagonist is walking
            self.cur_texture += 1
            if self.cur_texture >= len(self.walking_textures):
                self.cur_texture = 0
            self.texture = self.walking_textures[self.cur_texture]