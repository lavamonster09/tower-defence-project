from misc.ui import *
from misc.theme import *
from misc.constants import *
from screens.screen import Screen

class Menu(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (20,20,20)

        # buttons    
        self.add_item("btn_start",Button(BUTTON_DARK , rect=(SCREEN_WIDTH/2 - 100,250,200,100), text="START", on_click= self.btn_start_on_click))
        self.add_item("btn_settings", Button(BUTTON_DARK, rect = (SCREEN_WIDTH/2 - 150,400,300,100), text = "SETTINGS", on_click= self.btn_settings_on_click))

        # label
        self.add_item("label", Label(LABEL_DARK, rect = (SCREEN_WIDTH/2 - 150,0,300,200), text = "GAME"))

    def btn_start_on_click(self):
        self.screen_manager.current_screen = "game_select"
    
    def btn_settings_on_click(self):
        self.screen_manager.current_screen = "settings"
