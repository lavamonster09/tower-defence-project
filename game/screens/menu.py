from engine import *
from game.util.constants import *

class Menu(Screen):
    def __init__(self, screen_manager) -> None:
        screen_manager.game.sound_manager.play_music("Mixdown")
        super().__init__(screen_manager)
        self.back_color = (DARK_BACKGROUND_COLOR)

        # buttons    
        self.add_item("img_bkg", Image("assets\images/menu/menu_start.png", rect = (50,50,SCREEN_WIDTH,SCREEN_HEIGHT), positioning="relative"))
        self.add_item("btn_start",Button(BUTTON_DARK , rect=(50,40,200,100), text="START", on_click= self.btn_start_on_click, positioning="relative"))
        self.add_item("btn_settings", Button(BUTTON_DARK, rect = (50,60,300,100), text = "SETTINGS", on_click= self.btn_settings_on_click, positioning="relative"))
        self.add_item("btn_help", Button(BUTTON_DARK, rect = (3,95,50,50), text = get_icon_hex("help_outline"), positioning="relative", on_click= self.btn_help_on_click))

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
        return super().update()

    def btn_start_on_click(self):
        self.screen_manager.change_screen("game_select", 20)
    
    def btn_settings_on_click(self):
        self.screen_manager.change_screen("settings", 20)

    def btn_help_on_click(self):
        self.screen_manager.change_screen("help", 20)