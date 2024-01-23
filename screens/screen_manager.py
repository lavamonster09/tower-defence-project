import screens

class Screen_manager():
    def __init__(self, app) -> None:
        self.app = app
        self.current_screen = "menu"
        self.last_screen = "menu"
        self.before_last_screen = "menu"
        self.screens = {
            "menu": screens.Menu(self),
            "game_select": screens.Game_select(self),
            "settings": screens.Settings(self),
            "heroes": screens.Heroes(self)
        }
    
    def update(self):
        if self.last_screen != self.current_screen:
            self.before_last_screen = self.last_screen
            self.last_screen = self.current_screen
        self.screens[self.current_screen].update()
    
    def draw(self):
        self.screens[self.current_screen].draw()
