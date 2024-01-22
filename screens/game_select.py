from misc.ui import *
from misc.constants import *
from screens.screen import Screen

class Game_select(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (20,20,20)

        # Title
        self.add_item("Title", Label(LABEL_DARK, rect = (SCREEN_WIDTH/2 - 150,0,300,200), text = "GAME SELECT"))

        # btn_back
        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (0,0,50,50), text = "X", on_click= self.btn_back_on_click))

        # btn_start
        self.add_item("btn_heroes",Button(BUTTON_DARK , rect=(SCREEN_WIDTH/2 - 100,250,200,100), text="START"))
    
    def btn_back_on_click(self):
        self.screen_manager.current_screen = "menu"
    