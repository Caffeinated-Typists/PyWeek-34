import typing
import arcade

SCREEN_WIDTH:int = 600
SCREEN_HEIGTH:int = 800
SCREEN_TITLE:str = "PyWeek-34"

class MainMenu(arcade.View):

    def on_show(self)->None:
        """Display window on function call"""
        arcade.set_background_color(arcade.color.RED_BROWN)

    def on_draw(self)->None:
        """Instructions for layout of window"""
        self.clear()

class GameView(arcade.View):
    """Class for the handling all the game related functionality"""

    def __init__(self)->None:
        """Initialize the Game Menu class variables and utilities here"""
        super().__init__()

        arcade.set_background_color(arcade.color.RED_BROWN)

    def setup(self)->None:
        """Setup all the variables and maps here"""
        pass


def main()->None:
    """Main function for calling setup functions and running module"""
    window:arcade.Window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGTH, SCREEN_TITLE)
    menu_view:MainMenu = MainMenu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()