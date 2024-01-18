from screens.menu import Menu
from screens.settings import Settings
from screens.game_select import Game_select

class Screen_manager():
    def __init__(self) -> None:
        self.current_screen = "menu"
        self.screens = {
            "menu": Menu(self),
            "game_select": Game_select(self),
            "settings": Settings(self)
        }

    def update(self):
        self.screens[self.current_screen].update()
    
    def draw(self):
        self.screens[self.current_screen].draw()
