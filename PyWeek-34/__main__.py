import typing
import arcade
import arcade.gui
import copy
from time import time
import os
import sys

sys.path.append(os.getcwd() + r"\PyWeek-34")

from characters.protagonist import Protagonist
from clouds.clouds import Cloud
from foliage.foliage import Foliage
from env_objects.env_objects import EnvObject
from characters.ufo import UFO


#screen constants
SCREEN_WIDTH:int = 1000
SCREEN_HEIGHT:int = 480
SCREEN_TITLE:str = "PyWeek-34"

#Time constants
START_TIME:time = None
 
#scaling constants
TILE_SCALING:float = 0.5

#Physics Constants
GRAVITY:float = 0.6
GAME_SPEED:int = 8
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

# Game resources
# platforms 
CORNER_PIECE_LEFT:str = r"resources/Game Assets/deserttileset/png/Tile/1.png"
MIDDLE_PIECE:str = r"resources/Game Assets/deserttileset/png/Tile/2.png"  
CORNER_PIECE_RIGHT:str = r"resources/Game Assets/deserttileset/png/Tile/3.png"
#font
FONT:str = r"resources/Game Assets/GROBOLD.ttf"

#background
BACKGROUND:str = r"resources/Game Assets/deserttileset/png/BG.png"


#map constants
LAYER_PLATFORM:str = "Platform"
LAYER_CEILING:str = "Ceiling"
LAYER_PROTAGONIST:str = "Protagonist"
LAYER_CLOUD:str = "Clouds"
LAYER_ENVIRONMENT:str = "Environment"
LAYER_OBJECTS:str = "Objects"
LAYER_BULLETS:str = "Bullets"
LAYER_UFO:str = "UFO"
LAYER_TEMP:str = "Temp"

#set of objects to be used
OBJECTS:dict[str:typing.Optional] = {
    LAYER_CLOUD: Cloud, 
    LAYER_ENVIRONMENT: Foliage,
    LAYER_OBJECTS: EnvObject,
    LAYER_UFO: UFO
    }

def reset_dir()->bool:
    """Resets the current working directory to file path of this file"""
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)
    return True

class MainMenu(arcade.View):

    def __init__(self):
        """Initializes the main menu"""
        super().__init__()
        self.background:arcade.Texture = arcade.load_texture(BACKGROUND)
        self.manager:arcade.gui.UIManager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.load_font(FONT)
        start_style:dict[str:typing.Optional] = {
            "font_color": arcade.color.UFO_GREEN,
            "font_size": 40,
            "font_name": "GROBOLD",
            "bg_color": (15, 15, 15, 100),

            "bg_color_hover": (30, 30, 30, 100),
        }
        
        end_style:dict[str:typing.Optional] = copy.deepcopy(start_style)
        end_style["font_color"] = arcade.color.OUTRAGEOUS_ORANGE
        

        start:arcade.gui.UIFlatButton = arcade.gui.UIFlatButton(text="Start", x=SCREEN_WIDTH//3- 100, y=SCREEN_HEIGHT//3 - 50, width=200, height=100, style=start_style)
        exit_game:arcade.gui.UIFlatButton = arcade.gui.UIFlatButton(text="Exit", x= (2 * SCREEN_WIDTH//3) - 100, y=SCREEN_HEIGHT//3 - 50, width=200, height=100, style=end_style)
        self.manager.add(start)
        self.manager.add(exit_game)

    def on_show(self)->None:
        """Display window on function call"""
        arcade.set_background_color(arcade.color.RED_BROWN)


    def on_draw(self)->None:
        """Instructions for layout of window"""
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.manager.draw()


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """When mouse is clicked, start game"""
        if (x > SCREEN_WIDTH//3 - 100 and x < SCREEN_WIDTH//3 + 100) and (y > SCREEN_HEIGHT//3 - 50 and y < SCREEN_HEIGHT//3 + 50):
            game_view:GameView = GameView()
            self.window.show_view(game_view)

        elif (x > (2 * SCREEN_WIDTH//3) - 100 and x < (2 * SCREEN_WIDTH//3) + 100) and (y > SCREEN_HEIGHT//3 - 50 and y < SCREEN_HEIGHT//3 + 50):
            arcade.close_window()

class GameView(arcade.View):
    """Class for the handling all the game related functionality"""

    def __init__(self)->None:
        """Initialize the Game Menu class variables and utilities here"""
        super().__init__()

        arcade.set_background_color(arcade.color.RED_BROWN)

        self.scene:arcade.Scene = None
        self.background:arcade.Texture = None

        self.space_pressed:bool = False
        self.shoot_pressed:bool = False
        self.can_shoot:bool = True

        self.protagonist:arcade.Sprite = None

        self.score = 0

        self.physics_engine:arcade.PhysicsEnginePlatformer = None

    def setup(self)->None:
        """Setup all the variables and maps here"""
        self.background = arcade.load_texture(BACKGROUND)
        
        self.scene = arcade.Scene()

        #adding the layers
        self.scene.add_sprite_list(LAYER_PLATFORM)
        self.scene.add_sprite_list(LAYER_CLOUD)
        self.scene.add_sprite_list(LAYER_ENVIRONMENT)
        self.scene.add_sprite_list(LAYER_TEMP)
        self.scene.add_sprite_list(LAYER_OBJECTS)
        self.scene.add_sprite_list(LAYER_CEILING)
        self.scene.add_sprite_list(LAYER_PROTAGONIST)
        self.scene.add_sprite_list(LAYER_BULLETS)
        self.scene.add_sprite_list(LAYER_UFO)

        self.scene[LAYER_CLOUD].alpha = 100

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

        
        # temp sprite
        # temp_sprite:arcade.Sprite = arcade.Sprite(r"C:\Users\aniru\Downloads\sketch1662664053401.png", 0.3)
        # temp_sprite.center_x = 700
        # temp_sprite.center_y = PLATFORM_CENTER_Y + 100
        # self.scene.add_sprite(LAYER_ENVIRONMENT, temp_sprite)

        #environment sprites


        #adding initial object into the layers
        self.init_sprites(LAYER_CLOUD, 0, SCREEN_WIDTH, 2)
        self.init_sprites(LAYER_ENVIRONMENT, 0, SCREEN_WIDTH, 2)
        self.init_sprites(LAYER_OBJECTS, SCREEN_WIDTH, SCREEN_WIDTH * 2, 2)
        self.init_sprites(LAYER_UFO, SCREEN_WIDTH, SCREEN_WIDTH * 2, 2)

        self.generate_ceiling()

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.protagonist, gravity_constant = GRAVITY, platforms=self.scene[LAYER_PLATFORM], walls=self.scene[LAYER_CEILING]) 

        global START_TIME
        START_TIME = time()

    def on_show_view(self)->None:
        """Display window on function call"""
        self.setup()
        
    def on_draw(self)->None:
        """Instructions to generate the layout of the window"""
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.scene.draw()
        arcade.draw_text(f"TIME: {round(time() - START_TIME)}s", PLATFORM_HEIGHT/10, PLATFORM_WIDTH/2, arcade.csscolor.WHITE, 15)

    def on_update(self, delta_time: float):
        """Specify the computations at each refresh"""
        self.process_key_change()
        self.physics_engine.update()

        self.scene.update_animation(delta_time, [LAYER_PROTAGONIST])
        self.scene.update([LAYER_PROTAGONIST, LAYER_BULLETS])

        self.protagonist.set_pos_left(CHARACTER_LEFT)

        #moving elements in the scene
        self.move_and_pop(LAYER_PLATFORM, GAME_SPEED)
        self.move_and_pop(LAYER_CLOUD, CLOUD_SPEED)
        self.move_and_pop(LAYER_ENVIRONMENT, GAME_SPEED)
        self.move_and_pop(LAYER_OBJECTS, GAME_SPEED)
        self.move_and_pop(LAYER_UFO, GAME_SPEED)

        #adding platforms 
        self.clear_extra_bullets()

        if (len(self.scene[LAYER_PLATFORM]) < SCREEN_WIDTH // PLATFORM_WIDTH + 2):
            self.generate_platform(int(self.scene[LAYER_PLATFORM][-1].right) + PLATFORM_WIDTH // 2 - GAME_SPEED)

        #adding clouds, and foliage
        self.add_layer_sprites(LAYER_CLOUD, 2, 1, SCREEN_WIDTH)
        self.add_layer_sprites(LAYER_ENVIRONMENT, 2, 1, SCREEN_WIDTH)
        self.add_layer_sprites(LAYER_OBJECTS, 2, 1, SCREEN_WIDTH * 2)
        self.add_layer_sprites(LAYER_UFO, 2, 1, SCREEN_WIDTH)

        #checking for collision with env objects
        self.hit_list:list = arcade.check_for_collision_with_list(self.protagonist, self.scene[LAYER_OBJECTS])
        if len(self.hit_list) > 0:
            self.window.show_view(MainMenu())

        #checking for collisions with bullets
        for ufo in self.scene[LAYER_UFO]:
            hit_list = arcade.check_for_collision_with_list(ufo, self.scene[LAYER_BULLETS])
            if len(hit_list) > 0:
                #Update bullet damage to ufo
                pass
            for bullet in hit_list:
                bullet.remove_from_sprite_lists()


    def generate_platform(self, start:int):
        """Generates the platform"""
        for i in range(start, start + SCREEN_WIDTH * 2, PLATFORM_WIDTH):
            middle_sprite:arcade.Sprite = arcade.Sprite(MIDDLE_PIECE, TILE_SCALING, 
                                                        center_x=i, 
                                                        center_y=PLATFORM_CENTER_Y)
            self.scene.add_sprite(LAYER_PLATFORM, middle_sprite)

    def move_and_pop(self, layer:str, speed:int) -> None:
        """Moves all the sprites in the layer and pops the ones that are out of the screen"""
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
            if bullet.left > SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

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