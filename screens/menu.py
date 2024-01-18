from misc.ui import *
from misc.constants import *
from screens.screen import Screen

class Menu(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (20,20,20)
        self.add_item("btn_start", Button(rect = (SCREEN_WIDTH/2 - 100,250,200,100),
                             text = "START",
                             color = self.back_color,
                             border_radius = 10,
                             border_width = 2,
                             border_color = (150,150,150),
                             fore_color = (200,200,200),
                             hover_color = (50, 50, 50),
                             on_click= self.btn_start_on_click))
        self.add_item("btn_settings", Button(rect = (SCREEN_WIDTH/2 - 150,400,300,100),
                             text = "SETTINGS",
                             color = self.back_color,
                             border_radius = 10,
                             border_width = 2,
                             border_color = (150,150,150),
                             fore_color = (200,200,200),
                             hover_color = (50, 50, 50),
                             on_click= self.btn_settings_on_click))
        self.add_item("btn_label", Label(rect = (SCREEN_WIDTH/2 - 150,0,300,200),
                             text = "GAME",
                             color = (0,0,0),
                             fore_color = (150,150,150)))

    def btn_start_on_click(self):
        self.screen_manager.current_screen = "game_select"
    
    def btn_settings_on_click(self):
        self.screen_manager.current_screen = "settings"
