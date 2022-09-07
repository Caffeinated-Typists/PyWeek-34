import typing
import arcade
import os
os.chdir(os.getcwd() + r'\PyWeek-34')   #Changing current directory temporarily for importing rewuired character classes
from characters.protagonist import Protagonist

#screen constants
SCREEN_WIDTH:int = 1000
SCREEN_HEIGTH:int = 480
SCREEN_TITLE:str = "PyWeek-34"



#scaling constants
CHARACTER_SCALING:float = 1
TILE_SCALING:float = 0.5

#Physics Constants
GRAVITY:float = 1
GAME_SPEED:int = 1

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
LAYER_PROTAGONIST:str = "Protagonist"

LAYER_OPTIONS:dict[str:dict[str:typing.Optional]] = {
    LAYER_PLATFORM : {
        "use_spatial_hash": False, 
        "sprite_scaling": TILE_SCALING},
}


def validate()->bool:
    """Checks if the code is run from the proper directory"""
    if os.path.isdir("PyWeek-34"):
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        return True
    else: 
        return False

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

        self.left_pressed:bool = False
        self.right_pressed:bool = False
        self.up_pressed:bool = False

        self.protagonist:arcade.Sprite = None

        self.physics_engine:arcade.PhysicsEnginePlatformer = None

    def setup(self)->None:
        """Setup all the variables and maps here"""
        # map_file:str = "PyWeek-34/resources/Game Maps/main.json"
        self.background = arcade.load_texture(BACKGROUND)

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Platform")
        self.scene.add_sprite_list("Protagonist")

        arcade.set_background_color(arcade.color.RED_DEVIL)

        self.protagonist = Protagonist()
        self.protagonist.set_pos_x(CHARACTER_BOTTOM + self.protagonist.width // 2)
        self.protagonist.set_pos_y(CHARACTER_LEFT + self.protagonist.height // 2)
        self.scene.add_sprite(LAYER_PROTAGONIST, self.protagonist)


        #adding corner piece
        corner_sprite_left:arcade.Sprite = arcade.Sprite(CORNER_PIECE_LEFT, TILE_SCALING)
        corner_sprite_left.center_x = PLATFORM_CENTER_X
        corner_sprite_left.center_y = PLATFORM_CENTER_Y
        self.scene.add_sprite("Platform", corner_sprite_left)

        #adding middle sprites
        for i in range(PLATFORM_WIDTH + PLATFORM_CENTER_X, SCREEN_WIDTH, PLATFORM_WIDTH):
            middle_sprite:arcade.Sprite = arcade.Sprite(MIDDLE_PIECE, TILE_SCALING)
            middle_sprite.center_x = i  
            middle_sprite.center_y = PLATFORM_CENTER_Y
            self.scene.add_sprite("Platform", middle_sprite)                        

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.protagonist, gravity_constant = GRAVITY, platforms=self.scene["Platform"]) 



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
        self.process_key_change()
        self.protagonist.set_pos_left(CHARACTER_LEFT)
        for i in self.scene[LAYER_PLATFORM]:
            i.change_x=-GAME_SPEED

    def process_key_change(self) -> None:
        """Called after any recorded change in key to update the local variables appropriately"""

        if self.left_pressed and not self.right_pressed:
            self.protagonist.go_left()
        elif self.right_pressed and not self.left_pressed:
            self.protagonist.go_right()
        else:
            self.protagonist.stationary_x()

        if self.up_pressed and self.physics_engine.can_jump():
            self.protagonist.jump()

    def on_key_press(self, key: int, modifiers: int)->None:
        """Function to process the key presses of the user"""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True

        self.process_key_change()

    def on_key_release(self, key: int, modifiers: int):
        """Process when a key is released by the user"""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False

        self.process_key_change()


def main()->None:
    """Main function for calling setup functions and running module"""

    # if not validate():
        # raise Exception("Run the script in the correct directory")

    window:arcade.Window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGTH, SCREEN_TITLE)
    window.center_window = True
    menu_view:MainMenu = MainMenu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()