import typing
import arcade
import os

#screen constants
SCREEN_WIDTH:int = 1000
SCREEN_HEIGTH:int = 700
SCREEN_TITLE:str = "PyWeek-34"

#scaling constants
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

#map constants
LAYER_OPTIONS = {
    "Platform" : {"use_spatial_hash": True, "sprite_scaling": TILE_SCALING},
}


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

        

    def setup(self)->None:
        """Setup all the variables and maps here"""
        map_file = "PyWeek-34/resources/Game Maps/main.json"
        self.tile_map = arcade.load_tilemap(map_file, layer_options=LAYER_OPTIONS)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        

    def on_show_view(self):
        """Display window on function call"""
        self.setup()
        
    
    def on_draw(self):
        self.clear()
        self.scene.draw()


def main()->None:
    """Main function for calling setup functions and running module"""
    window:arcade.Window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGTH, SCREEN_TITLE)
    menu_view:MainMenu = MainMenu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()