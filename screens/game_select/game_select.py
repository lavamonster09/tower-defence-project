from misc.ui import *
from misc.constants import *
from screens.screen import Screen

class Game_select(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (DARK_BACKGROUND_COLOR)

        self.add_item("lbl_title", Label(LABEL_DARK, rect = (50,40,SCREEN_WIDTH,200), text = "TOWER DEFENCE", positioning="relative", font_size=100))

        # btn_start
        self.add_item("btn_play",Button(BUTTON_DARK , rect=(50,85,180,100), text="PLAY", positioning="relative", on_click= self.btn_heroes_on_click))
        self.add_item("btn_heroes",Button(BUTTON_DARK , rect=(30,87,270,100), text="HEROES", positioning="relative", on_click= self.btn_heroes_on_click))
        self.add_item("btn_upgrades",Button(BUTTON_DARK , rect=(70,87,270,100), text="UPGRADE", positioning="relative", on_click= self.btn_heroes_on_click))

        #btn_back
        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = "X", on_click= self.btn_back_on_click))

        #btn_settings
        self.add_item("btn_settings", Button(BUTTON_DARK, rect = (97,5,50,50), text = "{o}", positioning="relative", on_click= self.btn_settings_on_click))
    
    def btn_back_on_click(self):
        self.screen_manager.current_screen = "menu"
        
    def btn_heroes_on_click(self):
        self.screen_manager.current_screen = "heroes"

    def btn_settings_on_click(self):
        self.screen_manager.current_screen = "settings"