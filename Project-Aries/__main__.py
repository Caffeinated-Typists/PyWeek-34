import typing
import arcade
import arcade.gui
import copy
from time import time
from math import log2, floor, sin
import os
import sys

sys.path.append(os.getcwd() + r"\Project-Aries")

from characters.protagonist import Protagonist
from clouds.clouds import Cloud
from foliage.foliage import Foliage
from env_objects.env_objects import EnvObject
from characters.ufo import UFO
from characters.crawler import Crawler
from characters.spaceship import SpaceShip

#screen constants
SCREEN_WIDTH:int = 1000
SCREEN_HEIGHT:int = 480
SCREEN_TITLE:str = "Project Aries"

#Time constants
START_TIME:time = None

#score constants
TIME_MULTIPLIER:int = 4
ENEMY_MULTIPLIER:int = 20

#scaling constants
TILE_SCALING:float = 0.5

#Physics Constants
GRAVITY:float = 0.55
GAME_SPEED:int = 5
CLOUD_SPEED:float = 0.1 * GAME_SPEED

# Tile Constants
# 1. Platform
PLATFORM_WIDTH:int = int(128 * TILE_SCALING)
PLATFORM_HEIGHT:int = int(128 * TILE_SCALING)
PLATFORM_CENTER_X:int = PLATFORM_WIDTH // 2
PLATFORM_CENTER_Y:int = PLATFORM_HEIGHT // 2

#protagonist_position
CHARACTER_LEFT:int = 100
CHARACTER_BOTTOM:int = PLATFORM_HEIGHT 

#Bullet Constants
BULLET_DAMAGE:int = 100

#SpaceShip Constants
SPACESHIP_FREQ:int = 30
SHOOT_FREQ:int = 3

# Game resources
# platforms 
CORNER_PIECE_LEFT:str = r"resources/Game Assets/deserttileset/png/Tile/1.png"
MIDDLE_PIECE:str = r"resources/Game Assets/deserttileset/png/Tile/2.png"  
CORNER_PIECE_RIGHT:str = r"resources/Game Assets/deserttileset/png/Tile/3.png"
#font
FONT:str = r"resources/Game Assets/GROBOLD.ttf"
#background music
BACKGROUND_MUSIC:str = r"resources/Game Assets/Sounds/background-loop-melodic-techno.mp3"
END_SOUND:str = r"resources/Game Assets/Sounds/boxopen.ogg"
UFO_HIT_SOUND = r"characters/UFO Sprites/Bullet Impact 21.wav"

#background
BACKGROUND:str = r"resources/Game Assets/deserttileset/png/BG.png"


#map constants
LAYER_PLATFORM:str = "Platform"
LAYER_CEILING:str = "Ceiling"
LAYER_PROTAGONIST:str = "Protagonist"
LAYER_CLOUD:str = "Clouds"
LAYER_FOLIAGE:str = "Foliage"
LAYER_OBJECTS:str = "Objects"
LAYER_BULLETS:str = "Bullets"
LAYER_ENEMY_BULLETS:str = "Enemy_Bullets"
LAYER_UFO:str = "UFO"
LAYER_CRAWLER:str = "Crawlers"
LAYER_DEATH:str = "Death"
LAYER_SPACESHIP:str = "Spaceship"

#set of objects to be used
OBJECTS:dict[str:typing.Optional] = {
    LAYER_CLOUD: Cloud, 
    LAYER_FOLIAGE: Foliage,
    LAYER_OBJECTS: EnvObject,
    LAYER_UFO: UFO,
    LAYER_CRAWLER: Crawler,
    LAYER_SPACESHIP: SpaceShip,
}

def reset_dir()->bool:
    """Resets the current working directory to file path of this file"""
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)
    return True

class MainMenu(arcade.View):

    def __init__(self) -> None:
        """Initializes the main menu"""
        super().__init__()
        self.manager:arcade.gui.UIManager = None
        self.background:arcade.Texture = None
        arcade.load_font(FONT)
        self.setup()

    
    def setup(self) -> None:
        self.background = arcade.load_texture(BACKGROUND)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        start_style:dict[str:typing.Optional] = {
            "font_color": arcade.color.UFO_GREEN,
            "font_size": 40,
            "font_name": "GROBOLD",
            "bg_color": (15, 15, 15, 100),

            "bg_color_hover": (30, 30, 30, 100),
        }
        
        end_style:dict[str:typing.Optional] = copy.deepcopy(start_style)
        end_style["font_color"] = arcade.color.CORAL_RED
        

        start:arcade.gui.UIFlatButton = arcade.gui.UIFlatButton(text="Start", x=SCREEN_WIDTH//3- 100, y=SCREEN_HEIGHT//4 - 50, width=200, height=100, style=start_style)
        exit_game:arcade.gui.UIFlatButton = arcade.gui.UIFlatButton(text="Exit", x= (2 * SCREEN_WIDTH//3) - 100, y=SCREEN_HEIGHT//4 - 50, width=200, height=100, style=end_style)
        self.manager.add(start)
        self.manager.add(exit_game)

        self.title:arcade.Text = arcade.Text("Project: Aries", SCREEN_WIDTH//2, 2 * SCREEN_HEIGHT//3, arcade.color.WHITE, 65, width=100, font_name="consolas", align="left", anchor_x="center", anchor_y="center")

    def on_show(self)->None:
        """Display window on function call"""
        arcade.set_background_color(arcade.color.RED_BROWN)


    def on_draw(self)->None:
        """Instructions for layout of window"""
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.manager.draw()
        self.title.draw()


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Does different things depending on which button is pressed"""
        if (x > SCREEN_WIDTH//3 - 100 and x < SCREEN_WIDTH//3 + 100) and (y > SCREEN_HEIGHT//4 - 50 and y < SCREEN_HEIGHT//4 + 50):
            game_view:GameView = GameView()
            self.window.show_view(game_view)

        elif (x > (2 * SCREEN_WIDTH//3) - 100 and x < (2 * SCREEN_WIDTH//3) + 100) and (y > SCREEN_HEIGHT//4 - 50 and y < SCREEN_HEIGHT//4 + 50):
            arcade.close_window()

class GameView(arcade.View):
    """Class for the handling all the game related functionality"""

    def __init__(self)->None:
        """Initialize the Game Menu class variables and utilities here"""
        super().__init__()

        arcade.set_background_color(arcade.color.RED_BROWN)

        self.scene:arcade.Scene = None
        self.background:arcade.Texture = None
        self.manager:arcade.gui.UIManager = None
        self.space_pressed:bool = False
        self.shoot_pressed:bool = False
        self.can_shoot:bool = True

        self.protagonist:arcade.Sprite = None

        self.score = 0
        self.last_update:time = None

        self.spaceship_last_seen:time = None
        self.spaceship_motion:time = None

        self.physics_engine:arcade.PhysicsEnginePlatformer = None

        self.restart_style:dict[str:typing.Optional] = {
            "font_color": arcade.color.YELLOW,
            "font_size": 40,
            "font_name": "GROBOLD",
            "bg_color": (15, 15, 15, 100),

            "bg_color_hover": (30, 30, 30, 100),
        }

        self.end_style:dict[str:typing.Optional] = copy.deepcopy(self.restart_style)
        self.end_style["font_color"] = arcade.color.CORAL_RED

    def setup(self)->None:
        """Setup all the variables and maps here"""
        global GAME_SPEED
        self.background = arcade.load_texture(BACKGROUND)
        
        self.scene = arcade.Scene()
        self.manager = arcade.gui.UIManager()
        self.score = 0
        GAME_SPEED = 5

        #adding the layers
        self.scene.add_sprite_list(LAYER_PLATFORM)
        self.scene.add_sprite_list(LAYER_CLOUD)
        self.scene.add_sprite_list(LAYER_FOLIAGE)
        self.scene.add_sprite_list(LAYER_DEATH)
        self.scene.add_sprite_list(LAYER_OBJECTS)
        self.scene.add_sprite_list(LAYER_CEILING)
        self.scene.add_sprite_list(LAYER_PROTAGONIST)
        self.scene.add_sprite_list(LAYER_UFO)
        self.scene.add_sprite_list(LAYER_CRAWLER)
        self.scene.add_sprite_list(LAYER_SPACESHIP)
        self.scene.add_sprite_list(LAYER_BULLETS)
        self.scene.add_sprite_list(LAYER_ENEMY_BULLETS)

        self.scene[LAYER_CLOUD].alpha = 100
        #playing audio
        self.bg_player = arcade.play_sound(arcade.load_sound(BACKGROUND_MUSIC), looping=True)
        self.end_game = arcade.load_sound(END_SOUND)
        self.ufo_hit = arcade.load_sound(UFO_HIT_SOUND)

        #removing death layer(if present)

        #creating the protagonist
        self.protagonist = Protagonist()
        self.protagonist.set_pos_x(CHARACTER_BOTTOM + self.protagonist.width // 2)
        self.protagonist.set_pos_y(CHARACTER_LEFT + self.protagonist.height // 2)
        self.scene.add_sprite(LAYER_PROTAGONIST, self.protagonist)

        #adding corner piece
        corner_sprite_left:arcade.Sprite = arcade.Sprite(CORNER_PIECE_LEFT, TILE_SCALING)
        corner_sprite_left.center_x = PLATFORM_CENTER_X
        corner_sprite_left.center_y = PLATFORM_CENTER_Y
        self.scene.add_sprite(LAYER_PLATFORM, corner_sprite_left)

        #adding middle sprites
        self.generate_platform(PLATFORM_WIDTH + PLATFORM_CENTER_X)

        #environment sprites


        #adding initial object into the layers
        self.init_sprites(LAYER_CLOUD, 0, SCREEN_WIDTH, 2)
        self.init_sprites(LAYER_FOLIAGE, 0, SCREEN_WIDTH, 2)
        self.init_sprites(LAYER_OBJECTS, SCREEN_WIDTH, SCREEN_WIDTH * 2, 2)
        self.init_sprites(LAYER_UFO, SCREEN_WIDTH, SCREEN_WIDTH * 2, 2)
        # self.init_sprites(LAYER_CRAWLER, SCREEN_WIDTH, SCREEN_WIDTH * 2, 1)

        self.generate_ceiling()

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.protagonist, gravity_constant = GRAVITY, platforms=self.scene[LAYER_PLATFORM], walls=self.scene[LAYER_CEILING]) 

        global START_TIME
        START_TIME = time()
        self.last_update = START_TIME
        self.spaceship_last_seen = START_TIME
        self.spaceship_motion = None

    def on_show_view(self)->None:
        """Display window on function call"""
        self.setup()
        
    def on_draw(self)->None:
        """Instructions to generate the layout of the window"""
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.scene.draw()
        if not self.protagonist.is_dead:
            arcade.draw_text(f"SCORE: {round(self.score)}", PLATFORM_HEIGHT/10, PLATFORM_WIDTH/2, arcade.csscolor.WHITE, 15)
        self.manager.draw()
        if self.protagonist.is_dead:
            self.end_text.draw()
            self.score_text.draw()

    def on_update(self, delta_time: float):
        """Specify the computations at each refresh"""
        global GAME_SPEED
        if not self.protagonist.is_dead:
            self.score+=(time() - self.last_update)*TIME_MULTIPLIER
            self.last_update = time()
        self.process_key_change()
        self.physics_engine.update()

        self.scene.update_animation(delta_time, [LAYER_PROTAGONIST, LAYER_DEATH, LAYER_UFO, LAYER_CRAWLER])
        self.scene.update([LAYER_PROTAGONIST, LAYER_BULLETS, LAYER_CRAWLER, LAYER_ENEMY_BULLETS])

        self.protagonist.set_pos_x(CHARACTER_BOTTOM + self.protagonist.width // 2)

        #moving elements in the scene
        self.move_and_pop(LAYER_PLATFORM, GAME_SPEED)
        self.move_and_pop(LAYER_CLOUD, CLOUD_SPEED)
        self.move_and_pop(LAYER_FOLIAGE, GAME_SPEED)
        self.move_and_pop(LAYER_OBJECTS, GAME_SPEED)
        self.move_and_pop(LAYER_UFO, GAME_SPEED)
        self.move_and_pop(LAYER_DEATH, GAME_SPEED)
        self.move_and_pop(LAYER_CRAWLER, int(GAME_SPEED * 1.33))
        self.move_and_pop(LAYER_ENEMY_BULLETS, int(GAME_SPEED * 1.2))
        if (GAME_SPEED > 8) and (not self.protagonist.is_dead) and (len(self.scene[LAYER_SPACESHIP]) == 0) and ((time() - self.spaceship_last_seen) > SPACESHIP_FREQ):
            temp_spaceship:SpaceShip = SpaceShip()
            self.scene.add_sprite(LAYER_SPACESHIP, temp_spaceship)

        if (len(self.scene[LAYER_SPACESHIP]) != 0):
            if (time() - self.scene[LAYER_SPACESHIP][0].last_shot) > SHOOT_FREQ:
                self.scene[LAYER_SPACESHIP][0].can_shoot = True
            if self.scene[LAYER_SPACESHIP][0].can_shoot:
                self.scene[LAYER_SPACESHIP][0].shoot(self.scene)

            if self.spaceship_motion is None:
                if self.scene[LAYER_SPACESHIP][0].center_y < (3*(SCREEN_HEIGHT//5)):
                    self.spaceship_motion = time()
                else:
                    self.scene[LAYER_SPACESHIP][0].center_y -= 5
            else:
                self.scene[LAYER_SPACESHIP][0].center_y = int((3*(SCREEN_HEIGHT//5)) + (SCREEN_HEIGHT//5)*sin(time() - self.spaceship_motion))

        self.new_game_speed()

        #adding platforms 
        self.clear_extra_bullets()

        if (len(self.scene[LAYER_PLATFORM]) < SCREEN_WIDTH // PLATFORM_WIDTH + 2):
            self.generate_platform(int(self.scene[LAYER_PLATFORM][-1].right) + PLATFORM_WIDTH // 2 - GAME_SPEED)

        #adding clouds, and foliage
        self.add_layer_sprites(LAYER_CLOUD, 2, 1, SCREEN_WIDTH)
        self.add_layer_sprites(LAYER_FOLIAGE, 2, 1, SCREEN_WIDTH)
        self.add_layer_sprites(LAYER_OBJECTS, 2, 1, SCREEN_WIDTH * 2)
        self.add_layer_sprites(LAYER_UFO, 2, 1, SCREEN_WIDTH)
        if GAME_SPEED > 6:
            self.add_layer_sprites(LAYER_CRAWLER, 1, 1, SCREEN_WIDTH)

        #checking for collisions with bullets
        for ufo in self.scene[LAYER_UFO]:
            hit_list:list[arcade.Sprite] = arcade.check_for_collision_with_list(ufo, self.scene[LAYER_BULLETS])

            if len(hit_list) > 0:
                self.score += ENEMY_MULTIPLIER
                if ufo.update_bullet_damage(BULLET_DAMAGE):
                    arcade.play_sound(self.ufo_hit, volume=0.2)
                    ufo.play_dead_animation(self.scene)
                    ufo.remove_from_sprite_lists()
            for bullet in hit_list:
                bullet.remove_from_sprite_lists()

        for spaceship in self.scene[LAYER_SPACESHIP]:
            hit_list:list[arcade.Sprite] = arcade.check_for_collision_with_list(spaceship, self.scene[LAYER_BULLETS])

            if len(hit_list) > 0:
                self.score += 3*ENEMY_MULTIPLIER
                if ufo.update_bullet_damage(BULLET_DAMAGE):
                    arcade.play_sound(self.ufo_hit, volume=0.2)
                    spaceship.play_dead_animation(self.scene)
                    spaceship.remove_from_sprite_lists()
                    self.spaceship_last_seen = time()
                    self.spaceship_motion = None
            for bullet in hit_list:
                bullet.remove_from_sprite_lists()

        #checking for collision with env objects
        self.hit_list:list = arcade.check_for_collision_with_lists(self.protagonist, [self.scene[LAYER_OBJECTS], self.scene[LAYER_UFO], self.scene[LAYER_ENEMY_BULLETS], self.scene[LAYER_CRAWLER]])
        if len(self.hit_list) > 0:
            arcade.stop_sound(self.bg_player)
            arcade.play_sound(self.end_game)
            if self.protagonist.sound_player_flying: self.protagonist.sound_player_flying.pause()
            if self.protagonist.sound_player_ground: self.protagonist.sound_player_ground.pause()

            self.dead_protagonist:arcade.Sprite = self.protagonist.died(self.scene)
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.dead_protagonist, platforms=self.scene[LAYER_PLATFORM], gravity_constant=GRAVITY/2)
            GAME_SPEED = 0
            self.scene[LAYER_BULLETS].clear()
            self.scene[LAYER_OBJECTS].clear()
            self.scene[LAYER_UFO].clear()
            self.scene[LAYER_CRAWLER].clear()
            self.scene[LAYER_SPACESHIP].clear()
            self.scene[LAYER_CEILING].clear()
            self.scene[LAYER_ENEMY_BULLETS].clear()

            restart:arcade.gui.UIFlatButton = arcade.gui.UIFlatButton(text="Restart", x=SCREEN_WIDTH//3- 100, y=SCREEN_HEIGHT//4 - 50, width=200, height=100, style=self.restart_style)
            exit_game:arcade.gui.UIFlatButton = arcade.gui.UIFlatButton(text="Exit", x= (2 * SCREEN_WIDTH//3) - 100, y=SCREEN_HEIGHT//4 - 50, width=200, height=100, style=self.end_style)
            self.manager.add(restart)
            self.manager.add(exit_game)
            self.end_text:arcade.Text = arcade.Text("GAME OVER", SCREEN_WIDTH//2, 2 * SCREEN_HEIGHT//3, arcade.color.WHITE, 65, width=100, font_name="consolas", align="left", anchor_x="center", anchor_y="center")
            self.score_text:arcade.Text = arcade.Text(f"SCORE: {round(self.score)}", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.WHITE, 30, width=150, font_name="consolas", align="left", anchor_x="center")

    def generate_platform(self, start:int):
        """Generates the platform"""
        for i in range(start, start + SCREEN_WIDTH * 2, PLATFORM_WIDTH):
            middle_sprite:arcade.Sprite = arcade.Sprite(MIDDLE_PIECE, TILE_SCALING, 
                                                        center_x=i, 
                                                        center_y=PLATFORM_CENTER_Y)
            self.scene.add_sprite(LAYER_PLATFORM, middle_sprite)

    def move_and_pop(self, layer:str, speed:int) -> None:
        """Moves all the sprites in the layer and pops the ones that are out of the screen"""
        if len(self.scene[layer]) == 0:
            return

        for i in self.scene[layer]:
            i.center_x = i.center_x-speed
            
        if self.scene[layer][0].right <= 0:
            self.scene[layer].pop(0)
    
    def init_sprites(self, layer:str, start:int, step:int, no_of_sprites:int):
        """Initializes the sprites in the layer"""
        curr:int = 0
        while(curr < no_of_sprites):
            sprite:arcade.Sprite = OBJECTS[layer](start + curr * step)
            self.scene.add_sprite(layer, sprite)
            curr += 1

    
    def add_layer_sprites(self, layer:str, threshold:int, no_of_objects:int, start_position:int) -> None:
        """Adds new items(with start_position) to the specified layer, if number of objects is less than threshold"""
        if len(self.scene[layer]) < threshold:
            for i in range(no_of_objects):
                temp_sprite:arcade.Sprite = OBJECTS[layer](position=start_position)
                self.scene.add_sprite(layer, temp_sprite)

    def generate_ceiling(self):
        """Generates the ceiling for the Game Window"""
        ceiling_sprite:arcade.Sprite = arcade.Sprite(center_x=SCREEN_WIDTH/10, center_y=SCREEN_HEIGHT)
        ceiling_sprite.set_hit_box([[-SCREEN_WIDTH/10, -20], [SCREEN_WIDTH/5, 0]])
        self.scene.add_sprite(LAYER_CEILING, ceiling_sprite)

    def process_key_change(self) -> None:
        """Called after any recorded change in key to update the local variables appropriately"""

        if self.space_pressed:
            self.protagonist.fly()

        if self.shoot_pressed and self.can_shoot:
            self.protagonist.shoot(self.scene)
            self.can_shoot = False

    def on_key_press(self, key: int, modifiers: int)->None:
        """Function to process the key presses of the user"""

        if key == arcade.key.Q:
            self.shoot_pressed = True

        if key == arcade.key.SPACE or key == arcade.key.UP:
            self.space_pressed = True

    def on_key_release(self, key: int, modifiers: int):
        """Process when a key is released by the user"""
        
        if key == arcade.key.Q:
            self.shoot_pressed = False
            self.can_shoot = True

        if key == arcade.key.SPACE or key == arcade.key.UP:
            self.space_pressed = False

    def clear_extra_bullets(self) -> None:
        """Remove bullets which have left the screen out of Sprite list"""

        for bullet in self.scene[LAYER_BULLETS]:
            if (bullet.left > SCREEN_WIDTH) or (bullet.right < 0):
                bullet.remove_from_sprite_lists()

        for bullet in self.scene[LAYER_ENEMY_BULLETS]:
            if (bullet.left > SCREEN_WIDTH) or (bullet.right < 0):
                bullet.remove_from_sprite_lists()
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Restart and exit game"""
        if (x > SCREEN_WIDTH//3 - 100 and x < SCREEN_WIDTH//3 + 100) and (y > SCREEN_HEIGHT//4 - 50 and y < SCREEN_HEIGHT//4 + 50):
            self.setup()

        elif (x > (2 * SCREEN_WIDTH//3) - 100 and x < (2 * SCREEN_WIDTH//3) + 100) and (y > SCREEN_HEIGHT//4 - 50 and y < SCREEN_HEIGHT//4 + 50):
            arcade.close_window()

    def new_game_speed(self):
        """Updates the speed"""
        global GAME_SPEED
        GAME_SPEED = min(5 + int((time() - START_TIME) // 30), 14)
        
        if GAME_SPEED > 11:
            self.protagonist.start_running()
        
        if self.protagonist.is_dead:
            GAME_SPEED = 0

def main()->None:
    """Main function for calling setup functions and running module"""
    reset_dir()

    window:arcade.Window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.center_window = True
    menu_view:MainMenu = MainMenu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()