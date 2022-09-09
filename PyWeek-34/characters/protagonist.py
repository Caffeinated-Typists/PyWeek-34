from enum import Flag
import typing
from unittest.mock import NonCallableMagicMock
import arcade

#Constants for Protagonist
PROTAGONIST_SCALING:float = 0.22
PROTAGONIST_SPEED:int = 10
PROTAGONIST_JUMP_SPEED:int = 20
PROTAGONIST_JETPACK_ACCLRN:int = 1

#Constants for bullets
LAYER_BULLETS:str = "Bullets"
BULLET_SPEED:int = 10
BULLET_DAMAGE:int = 100

#Constants for getting Images from Sprite List
IMAGE_PIXEL_HEIGHT:int = 599
IMAGE_PIXEL_WIDTH:int = 692

class Protagonist(arcade.Sprite):

    def __init__(self) -> None:
        """Initialize the character"""
        super().__init__(scale = PROTAGONIST_SCALING)
        self.idle_texture:arcade.Texture = arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_standing_idle.png", x = 0, y = 0, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) 
        self.flying_textures:list[arcade.Texture] = [arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_flying_no_movement.png", x = i%5 * IMAGE_PIXEL_WIDTH, y = i//5 * IMAGE_PIXEL_HEIGHT, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) for i in range(10)]
        self.shooting_flying_texture:list[arcade.Texture] = [arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_with_weapon_standing_shoot.png")]
        self.falling_textures:list[arcade.Texture] = [arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_standing_run.png", x = i%5 * IMAGE_PIXEL_WIDTH, y = i//5 * IMAGE_PIXEL_HEIGHT, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) for i in range(15)]
        self.shooting_falling_textures:list[arcade.Texture] = [arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_standing_run.png", x = i%5 * IMAGE_PIXEL_WIDTH, y = i//5 * IMAGE_PIXEL_HEIGHT, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) for i in range(15)]
        self.running_textures:list[arcade.Texture] = [arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_standing_run.png", x = i%5 * IMAGE_PIXEL_WIDTH, y = i//5 * IMAGE_PIXEL_HEIGHT, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) for i in range(15)]
        self.walking_textures:list[arcade.Texture] = [arcade.load_texture("characters\jetpack character\spritesheets\__jet_pack_man_no_weapon_white_helmet_standing_walk.png", x = i%5 * IMAGE_PIXEL_WIDTH, y = i//5 * IMAGE_PIXEL_HEIGHT, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) for i in range(15)]
        self.dying_flying_textures:list[arcade.Texture] = None
        self.dying_walking_textures:list[arcade.Texture] = None
        self.texture:arcade.Texture = self.idle_texture

        self.is_flying:bool = False
        self.is_falling:bool = False
        self.is_running:bool = False
        self.can_shoot:bool = False
        self.cur_texture:int = 0

        self.horizontal_vel:int = PROTAGONIST_SPEED
        self.jump_vel:int = PROTAGONIST_JUMP_SPEED
        self.jetpack_accln:int = PROTAGONIST_JETPACK_ACCLRN
        self.set_hit_box([[-33, 240], [33, -240]])
        
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

    def fly(self) -> None:
        """Update the y-velocity for jumping"""
        self.update_vel_y(self.jetpack_accln)

    def shoot(self, scene:arcade.scene) -> None:
        """Shoot bullets at the opponent"""
        bullet:arcade.Sprite = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
        bullet.center_x = self.center_x
        bullet.center_y = self.center_y
        bullet.change_x = BULLET_SPEED
        scene.add_sprite(LAYER_BULLETS, bullet)

    def update_animation(self, delta_time: float) -> None:
        """Update the animation of the Protagonist at every call"""

        if self.change_y > -0.5:
            self.is_flying = True
            self.is_falling = False
            self.is_running = False
        elif self.change_y < -0.5:
            self.is_flying = False
            self.is_falling = True 
            self.is_running = False
        else:
            self.is_flying = False
            self.is_falling = False
            self.is_running = True

        if self.is_flying:          #If the Protagonist has Jetpack
            self.cur_texture += 1
            if self.cur_texture >= len(self.flying_textures):
                self.cur_texture = 0
            self.texture = self.flying_textures[self.cur_texture]
        elif self.is_falling:       #If the Protagonist is jumping
                self.cur_texture += 1
                if self.cur_texture >= len(self.falling_textures):
                    self.cur_texture = 0
                self.texture = self.falling_textures[self.cur_texture]
        elif self.is_running:       #If the Protagonist is running
            self.cur_texture += 1
            if self.cur_texture >= len(self.running_textures):
                self.cur_texture = 0
            self.texture = self.running_textures[self.cur_texture]
        else:                       #If the Protagonist is walking
            self.cur_texture += 1
            if self.cur_texture >= len(self.walking_textures):
                self.cur_texture = 0
            self.texture = self.walking_textures[self.cur_texture]