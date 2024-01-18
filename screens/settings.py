from misc.ui import *
from misc.constants import *
from screens.screen import Screen

class Settings(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.add_item(Label(rect = (SCREEN_WIDTH/2 - 150,0,300,200),
                             text = "SETTINGS",
                             color = (0,0,0),
                             fore_color = (150,150,150)))