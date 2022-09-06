import typing
import arcade
import os
os.chdir(os.getcwd() + r'\PyWeek-34')   #Changing current directory temporarily for importing rewuired character classes
from characters.protagonist import Protagonist

#screen constants
SCREEN_WIDTH:int = 1000
SCREEN_HEIGTH:int = 700
SCREEN_TITLE:str = "PyWeek-34"

#scaling constants
CHARACTER_SCALING:float = 1
TILE_SCALING:float = 0.5

#Physics Constants
GRAVITY:float = 1

#map constants
LAYER_OPTIONS:dict[str:dict[str:typing.Optional]] = {
    "Platform" : {"use_spatial_hash": True, "sprite_scaling": TILE_SCALING},
}
LAYER_PROTAGONIST = "Protagonist"

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

        self.left_pressed:bool = False
        self.right_pressed:bool = False
        self.up_pressed:bool = False

        self.protagonist:arcade.Sprite = None

        self.physics_engine:arcade.PhysicsEnginePlatformer = None

    def setup(self)->None:
        """Setup all the variables and maps here"""
        # map_file:str = "PyWeek-34/resources/Game Maps/main.json"
        map_file:str = "resources/Game Maps/main.json"
        self.tile_map = arcade.load_tilemap(map_file, layer_options=LAYER_OPTIONS)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.protagonist = Protagonist()
        self.protagonist.set_pos_x(500)
        self.protagonist.set_pos_y(350)
        self.scene.add_sprite(LAYER_PROTAGONIST, self.protagonist)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.protagonist, gravity_constant = GRAVITY, walls = self.scene["Platform"]) 

    def on_show_view(self)->None:
        """Display window on function call"""
        self.setup()
        
    def on_draw(self)->None:
        """Instructions to generate the layout of the window"""
        self.clear()
        self.scene.draw()

    def on_update(self, delta_time: float):
        """Specify the computations at each refresh"""
        self.physics_engine.update()

        self.process_key_change()

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