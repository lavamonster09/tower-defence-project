class ScreenManager():
    def __init__(self, game, startup_screen: str, screens: dict) -> None:
        self.game = game 
        self.current_screen = startup_screen  # The screen that is currently active
        self.last_screen = startup_screen  # The screen that was active last
        self.before_last_screen = startup_screen  # The screen that was active before the last screen
        self.change_in = 0  # Counter for delayed screen change
        self.change_to = startup_screen  
        self.counter = 0  # Counter to keep track of frames for delayed screen change
        self.screens = screens  
        
        # Initialize each screen by passing the screen manager reference
        for screen in self.screens:
            self.screens[screen] = self.screens[screen](self)
    
    def update(self):
        # Handle delayed screen change
        if self.change_in > 0:
            self.counter += 1
            if self.counter > self.change_in:
                self.counter = 0
                self.change_in = 0
                # Transfer cursor radius to new screen
                self.screens[self.change_to].cursor_rad = self.screens[self.current_screen].cursor_rad
                self.current_screen = self.change_to
        
        # Check if the screen has changed
        if self.last_screen != self.current_screen:
            self.screens[self.current_screen].on_open()  
            self.before_last_screen = self.last_screen  
        self.last_screen = self.current_screen  
        self.screens[self.current_screen].update()  

    def add_screen(self, screen_name, screen):
        # Add a new screen to the screen manager
        self.screens[screen_name] = screen
    
    def draw(self):
        # Draw the current screen
        if self.last_screen == self.current_screen:
            self.screens[self.current_screen].draw()
        else:
            self.update() 
            self.draw() 

    def change_screen(self, screen, change_in=0):
        # Change to a different screen with an optional delay
        self.screens[self.current_screen].on_close() 
        self.change_in = change_in  
        self.change_to = screen 