import screens

class Screen_manager():
    def __init__(self) -> None:
        self.current_screen = "menu"
        self.screens = {
            "menu": screens.Menu(self),
            "game_select": screens.Game_select(self),
            "settings": screens.Settings(self)
        }
    
    def update(self):
        self.screens[self.current_screen].update()
    
    def draw(self):
        self.screens[self.current_screen].draw()
