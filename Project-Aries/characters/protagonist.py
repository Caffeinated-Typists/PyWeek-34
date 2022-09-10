import sys, os
import typing
import arcade
sys.path.append(os.getcwd() + r"\Project-Aries")
from characters.enemy import Death_Sprite

#Constants for Protagonist
PROTAGONIST_SCALING:float = 0.22
PROTAGONIST_SPEED:int = 10
PROTAGONIST_JUMP_SPEED:int = 20
PROTAGONIST_JETPACK_ACCLRN:int = 1

#Constants for bullets
LAYER_BULLETS:str = "Bullets"
BULLET_SCALE:float = 0.8
BULLET_SPEED:int = 10
BULLET_DAMAGE:int = 100
BULLET_MARGIN_X:int = 50
BULLET_MARGIN_Y:int = 0

#Constants for getting Images from Sprite List
IMAGE_PIXEL_HEIGHT:int = 599
IMAGE_PIXEL_WIDTH:int = 692
FLYING_IMAGE_PIXEL_WIDTH:int = 881
FLYING_IMAGE_PIXEL_HEIGHT:int = 639

#sounds
SOUND_WALKING:str = r"characters/jetpack character/sounds/steps_platform.ogg"
SOUND_FLYING_START:str = r"characters/jetpack character/sounds/start.ogg"
SOUND_FLYING_MAIN:str = r"characters/jetpack character/sounds/main.ogg"
SOUND_FLYING_END:str = r"characters/jetpack character/sounds/ending.ogg"
PEW:str = r"characters/jetpack character/sounds/pew.wav"

LAYER_DEATH:str = "Death"


class Protagonist(arcade.Sprite):

    def __init__(self) -> None:
        """Initialize the character"""
        super().__init__(scale = PROTAGONIST_SCALING)
        self.idle_texture:arcade.Texture = arcade.load_texture("characters/jetpack character/no_weapon_white_helmet_standing_idle.png", x = 0, y = 0, width = IMAGE_PIXEL_WIDTH, height = IMAGE_PIXEL_HEIGHT) 
        self.flying_textures:list[arcade.Texture] = self.add_animation("no_weapon_white_helmet_flying", 15)
        self.with_gun_flying_textures:list[arcade.Texture] = self.add_animation("with_weapon_flying", 15)
        self.shooting_flying_textures:list[arcade.Texture] = self.add_animation("with_weapon_flying_shoot", 10)
        self.falling_textures:list[arcade.Texture] = self.add_animation("no_weapon_white_helmet_standing_idle", 15)
        self.with_gun_falling_textures:list[arcade.Texture] = self.add_animation("with_weapon_standing_idle", 15)
        self.shooting_falling_textures:list[arcade.Texture] = self.add_animation("with_weapon_standing_shoot", 5)
        self.running_textures:list[arcade.Texture] = self.add_animation("no_weapon_white_helmet_standing_run", 15)
        self.walking_textures:list[arcade.Texture] = self.add_animation("no_weapon_white_helmet_standing_walk", 15)

        self.with_gun_dying_flying_textures:list[arcade.Texture] = self.add_animation("with_weapon_flying_die", 5)
        self.dying_flying_textures:list[arcade.Texture] = self.add_animation("no_weapon_white_helmet_flying_die", 5)
        self.dying_walking_textures:list[arcade.Texture] = self.add_animation("no_weapon_white_helmet_standing_die", 5)
        self.texture:arcade.Texture = self.idle_texture
        self.textures:list[arcade.Texture] = None      

        self.is_flying:bool = False
        self.is_falling:bool = False
        self.is_running:bool = False
        self.is_on_ground:bool = False
        self.can_shoot:bool = False
        self.is_shooting:bool = False
        self.is_dead:bool = False
        self.cur_texture:int = 0

        self.horizontal_vel:int = PROTAGONIST_SPEED
        self.jump_vel:int = PROTAGONIST_JUMP_SPEED
        self.jetpack_accln:int = PROTAGONIST_JETPACK_ACCLRN
        self.set_hit_box([[-55, 240], [55, -240]])

        self.walking_sound = arcade.load_sound(SOUND_WALKING)
        self.flying_start_sound = arcade.load_sound(SOUND_FLYING_START)
        self.flying_main_sound = arcade.load_sound(SOUND_FLYING_MAIN)
        self.flying_end_sound = arcade.load_sound(SOUND_FLYING_END)
        self.pew = arcade.load_sound(PEW)


        self.sound_player_ground = None
        self.sound_player_flying = None
        self.start_shooting()
        
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

    def reset_animation_count(self) -> None:
        """Helper function to reset the animation count"""
        self.cur_texture = 0

    def start_running(self) -> None:
        """Protagonist will run instead of walk now"""
        self.is_running = True

    def start_shooting(self) -> None:
        """Protagonist can now use his gun while flying"""
        self.can_shoot = True

    def fly(self) -> None:
        """Update the y-velocity for jumping"""
        self.update_vel_y(self.jetpack_accln)

    def died(self, scene:arcade.Scene) -> None:
        """Protagonist has been killed"""
        self.is_dead = True
        if self.is_falling or self.is_flying:
            if self.can_shoot:
                self.textures = self.with_gun_dying_flying_textures
            else:
                self.textures = self.dying_flying_textures
        else:
            self.textures = self.dying_walking_textures
        self.remove_from_sprite_lists()
        self.is_dead = True
        death_sprite:Death_Sprite = Death_Sprite(self.textures, PROTAGONIST_SCALING, dont_delete = True)
        death_sprite.center_x = self.center_x
        death_sprite.center_y = self.center_y
        scene.add_sprite(LAYER_DEATH, death_sprite)

    def shoot(self, scene:arcade.scene) -> None:
        """Shoot bullets at the opponent"""
        if not self.can_shoot:
            return
        if self.is_on_ground:             #Can't shoot bullets on ground
            return
        bullet:arcade.Sprite = arcade.Sprite("characters\jetpack character\laserRed16.png", BULLET_SCALE)
        bullet.center_x = self.center_x + BULLET_MARGIN_X
        bullet.center_y = self.center_y + BULLET_MARGIN_Y
        bullet.change_x = BULLET_SPEED
        scene.add_sprite(LAYER_BULLETS, bullet)
        self.is_shooting = True
        arcade.play_sound(self.pew, volume=0.3)



    def animate_shooting(self) -> None:
        """Helper function to animate the object while shooting"""
        self.cur_texture += 1
        if self.cur_texture >= len(self.textures):
            self.reset_animation_count()
            self.is_shooting = False
        self.texture = self.textures[self.cur_texture]

    def animate(self) -> None:
        """Helper function to animate the object"""
        self.cur_texture += 1
        if self.cur_texture >= len(self.textures):
            self.reset_animation_count()
        self.texture = self.textures[self.cur_texture]

    def update_animation(self, delta_time: float) -> None:
        """Update the animation of the Protagonist at every call"""
        initial_state:list[bool] = [self.is_flying, self.is_falling, self.is_on_ground]

        if (self.change_y > 0) or (self.change_y > -0.5 and self.center_y > 400):
            # inset flying sound here
            self.is_flying = True
            self.is_falling = False
            self.is_on_ground = False
        elif self.change_y < -0.5:
            self.is_flying = False
            self.is_falling = True 
            self.is_on_ground = False
        else:
            self.is_flying = False
            self.is_falling = False
            self.is_on_ground = True

        final_state:list[bool] = [self.is_flying, self.is_falling, self.is_on_ground]
        
        if  (not initial_state[2]) and (final_state[2]):
            self.sound_player_ground = self.walking_sound.play(loop=True, volume=0.5)
        elif (not final_state[2]) and (initial_state[2]):
            if self.sound_player_ground:
                self.sound_player_ground.pause()
        
        if (not initial_state[0]) and (final_state[0]):
            self.flying_start_sound.play(volume=0.5)
            self.sound_player_flying = self.flying_main_sound.play(loop=True, volume=0.5)

        elif (not final_state[0]) and (initial_state[0]):
            self.flying_end_sound.play(volume=0.5)
            if self.sound_player_flying:
                self.sound_player_flying.pause()

        if self.is_flying:
            if self.is_shooting:
                self.textures = self.shooting_flying_textures
                self.animate_shooting()
            elif self.can_shoot:
                self.textures = self.with_gun_flying_textures
                self.animate()
            else:
                self.textures = self.flying_textures
                self.animate()
        elif self.is_falling:
            if self.is_shooting:
                self.textures = self.shooting_falling_textures
                self.animate_shooting()
            elif self.can_shoot:
                self.textures = self.with_gun_falling_textures
                self.animate()
            else:
                self.textures = self.falling_textures
                self.animate()
        elif self.is_running:
            self.textures = self.running_textures
            self.animate()
        else:
            self.textures = self.walking_textures
            self.animate()
        

    def add_animation(self, spriteSheet:str, count:int) -> list[arcade.Texture]:
        """Add animation sprites to the protagonist"""
        rval:list[arcade.Texture] = []
        for i in range(count):
            column:int = (i % 5) + 1
            row:int = (i // 5) + 1
            texture = arcade.load_texture(f"characters/jetpack character/{spriteSheet}/row-{row}-column-{column}.png")
            rval.append(texture)
        
        return rval
    
    
        
