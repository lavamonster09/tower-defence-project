class ScreenManager():
    def __init__(self, game, startup_screen : str, screens: dict) -> None:
        self.game = game
        self.current_screen = startup_screen
        self.last_screen = startup_screen
        self.before_last_screen = startup_screen
        self.change_in = 0
        self.change_to = startup_screen
        self.counter = 0 
        self.screens = screens
        for screen in self.screens:
            self.screens[screen] = self.screens[screen](self)
    
    def update(self):
        if self.change_in > 0:
            self.counter += 1
            if self.counter > self.change_in:
                self.counter = 0
                self.change_in = 0
                self.screens[self.change_to].cursor_rad = self.screens[self.current_screen].cursor_rad
                self.current_screen = self.change_to
        if self.last_screen != self.current_screen:
            self.screens[self.current_screen].on_open()
            self.before_last_screen = self.last_screen
        self.last_screen = self.current_screen
        self.screens[self.current_screen].update()

    def add_screen(self, screen_name, screen):
        self.screens[screen_name] = screen
    
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