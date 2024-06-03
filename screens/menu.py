from misc.ui import *
from misc.theme import *
from misc.constants import *
from screens.screen import Screen

class Menu(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (DARK_BACKGROUND_COLOR)

        # buttons    
        self.add_item("img_bkg", Image("assets\images/null.png", rect = (50,50,SCREEN_WIDTH,SCREEN_HEIGHT), positioning="relative"))
        self.add_item("btn_start",Button(BUTTON_DARK , rect=(50,40,200,100), text="START", on_click= self.btn_start_on_click, positioning="relative"))
        self.add_item("btn_settings", Button(BUTTON_DARK, rect = (50,60,300,100), text = "SETTINGS", on_click= self.btn_settings_on_click, positioning="relative"))

        # label
        self.add_item("label", Label(LABEL_DARK, rect = (50,10,SCREEN_WIDTH,200), text = "GAME", positioning="relative", font_size=100))

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
        return super().update()

    def btn_start_on_click(self):
        self.screen_manager.change_screen("game_select", 20)
    
    def btn_settings_on_click(self):
        self.screen_manager.change_screen("settings", 20)
