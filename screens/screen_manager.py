import screens
from game.game import Game

class ScreenManager():
    def __init__(self, app) -> None:
        self.app = app
        self.current_screen = "menu"
        self.last_screen = "menu"
        self.before_last_screen = "menu"
        self.change_in = 0
        self.change_to = "menu"
        self.counter = 0 
        self.screens = {
            "menu": screens.Menu(self),
            "game_select": screens.Game_select(self),
            "game": Game(self),
            "settings": screens.Settings(self),
            "heroes": screens.Heroes(self),
            "upgrades": screens.Upgrades(self)
        }
    
    def update(self):
        if self.change_in > 0:
            self.counter += 1
            if self.counter > self.change_in:
                self.counter = 0
                self.change_in = 0
                self.current_screen = self.change_to
        if self.last_screen != self.current_screen:
            self.screens[self.current_screen].on_open()
            self.before_last_screen = self.last_screen
        self.last_screen = self.current_screen
        self.screens[self.current_screen].update()
    
    def draw(self):
        if self.last_screen == self.current_screen:
            self.screens[self.current_screen].draw()
        else:
            self.update()
            self.draw()

    def change_screen(self, screen, change_in = 0):
        self.screens[self.current_screen].on_close()
        self.change_in = change_in
        self.change_to = screen