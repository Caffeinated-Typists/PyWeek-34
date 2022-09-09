import typing
import arcade
import os
import sys
sys.path.append(os.getcwd() + r"\PyWeek-34")
from characters.protagonist import Protagonist

#screen constants
SCREEN_WIDTH:int = 1000
SCREEN_HEIGTH:int = 480
SCREEN_TITLE:str = "PyWeek-34"


 
#scaling constants
TILE_SCALING:float = 0.5

#Physics Constants
GRAVITY:float = 0.6
GAME_SPEED:int = 10

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

#background
BACKGROUND:str = r"resources/Game Assets/deserttileset/png/BG.png"


#map constants

LAYER_PLATFORM:str = "Platform"
LAYER_CEILING:str = "Ceiling"
LAYER_PROTAGONIST:str = "Protagonist"
LAYER_BULLETS:str = "Bullets"

LAYER_OPTIONS:dict[str:dict[str:typing.Optional]] = {
    LAYER_PLATFORM : {
        "use_spatial_hash": False, 
        "sprite_scaling": TILE_SCALING},
    LAYER_CEILING : {
        "use_spatial_hash": False},
}


def reset_dir()->bool:
    """Resets the current working directory to file path of this file"""
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)
    return True

class MainMenu(arcade.View):

    def on_show(self)->None:
        """Display window on function call"""
        arcade.set_background_color(arcade.color.RED_BROWN)

    def on_draw(self)->None:
        """Instructions for layout of window"""
        self.clear()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """When mouse is clicked, start game"""
        game_view:GameView = GameView()
        self.window.show_view(game_view)

class GameView(arcade.View):
    """Class for the handling all the game related functionality"""

    def __init__(self)->None:
        """Initialize the Game Menu class variables and utilities here"""
        super().__init__()

        arcade.set_background_color(arcade.color.RED_BROWN)

        self.scene:arcade.Scene = None
        self.tile_map:arcade.tilemap.TileMap = None
        self.background:arcade.Texture = None

        self.space_pressed:bool = False
        self.shoot_pressed:bool = False
        self.can_shoot:bool = True

        self.protagonist:arcade.Sprite = None

        self.physics_engine:arcade.PhysicsEnginePlatformer = None

    def setup(self)->None:
        """Setup all the variables and maps here"""
        # map_file:str = "PyWeek-34/resources/Game Maps/main.json"
        self.background = arcade.load_texture(BACKGROUND)

        self.scene = arcade.Scene()
        self.scene.add_sprite_list(LAYER_PLATFORM)
        self.scene.add_sprite_list(LAYER_CEILING)
        self.scene.add_sprite_list(LAYER_PROTAGONIST)
        self.scene.add_sprite_list(LAYER_BULLETS)

        arcade.set_background_color(arcade.color.RED_DEVIL)

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

        self.generate_ceiling()

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.protagonist, gravity_constant = GRAVITY, platforms=self.scene[LAYER_PLATFORM], walls=self.scene[LAYER_CEILING]) 

    def on_show_view(self)->None:
        """Display window on function call"""
        self.setup()
        
    def on_draw(self)->None:
        """Instructions to generate the layout of the window"""
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGTH, self.background)
        self.scene.draw()

    def on_update(self, delta_time: float):
        """Specify the computations at each refresh"""
        self.physics_engine.update()

        self.scene.update_animation(delta_time, [LAYER_PROTAGONIST])
        self.scene.update([LAYER_PROTAGONIST, LAYER_BULLETS])

        self.process_key_change()
        self.protagonist.set_pos_left(CHARACTER_LEFT)
        for i in self.scene[LAYER_PLATFORM]:
            i.change_x=-GAME_SPEED
            
        if self.scene[LAYER_PLATFORM][0].right <= 0:
            self.scene[LAYER_PLATFORM].pop(0)

        self.clear_extra_bullets()

        if (len(self.scene[LAYER_PLATFORM]) < SCREEN_WIDTH // PLATFORM_WIDTH + 2):
            self.generate_platform(int(self.scene[LAYER_PLATFORM][-1].right) + PLATFORM_WIDTH // 2 - GAME_SPEED)

    def generate_platform(self, start:int):
        """Generates the platform"""
        for i in range(start, start + SCREEN_WIDTH * 2, PLATFORM_WIDTH):
            middle_sprite:arcade.Sprite = arcade.Sprite(MIDDLE_PIECE, TILE_SCALING, 
                                                        center_x=i, 
                                                        center_y=PLATFORM_CENTER_Y)
            self.scene.add_sprite(LAYER_PLATFORM, middle_sprite)

    def generate_ceiling(self):
        """Generates the ceiling for the Game Window"""
        ceiling_sprite:arcade.Sprite = arcade.Sprite(center_x=SCREEN_WIDTH/10, center_y=SCREEN_HEIGTH)
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

        if key == arcade.key.SPACE:
            self.space_pressed = True

        self.process_key_change()

    def on_key_release(self, key: int, modifiers: int):
        """Process when a key is released by the user"""
        
        if key == arcade.key.Q:
            self.shoot_pressed = False
            self.can_shoot = True

        if key == arcade.key.SPACE:
            self.space_pressed = False

        self.process_key_change()

    def clear_extra_bullets(self) -> None:
        """Remove bullets which have left the screen out of Sprite list"""

        for bullet in self.scene[LAYER_BULLETS]:
            if bullet.left > SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

def main()->None:
    """Main function for calling setup functions and running module"""
    reset_dir()

    window:arcade.Window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGTH, SCREEN_TITLE)
    window.center_window = True
    menu_view:MainMenu = MainMenu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()