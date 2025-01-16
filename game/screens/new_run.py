from engine import *
from game.util.constants import *

class New_run(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (DARK_BACKGROUND_COLOR)

        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("arrow_back"), on_click= self.btn_back_on_click))
        
        self.add_item("btn_startrun", Button(BUTTON_DARK , rect=(20,87,400,100), text = "start", on_click= self.btn_start_on_click, positioning="relative"))
        self.add_item("lbl_newrun", Label(LABEL_DARK, rect=(50,5,180,50), text="New Run", font_size=40, positioning="relative"))

        self.add_item("large_hero", Image("assets/images/heroes/lime_large.png", rect = (80,50,SCREEN_WIDTH/4.5,SCREEN_HEIGHT/2), positioning="relative"))
        self.add_item("hero_title", Label(LABEL_DARK, rect = (80,25,SCREEN_WIDTH/4,100), positioning="relative", font_size=30, text="Selected hero"))
        self.add_item("hero_name", Label(LABEL_DARK, rect = (80,75,SCREEN_WIDTH/4,100), positioning="relative", font_size=30, text="Selected hero"))
        

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.btn_back_on_click()
        return super().update()

    def btn_back_on_click(self):
        self.screen_manager.change_screen(self.screen_manager.before_last_screen, 20)

    def btn_start_on_click(self):
        self.screen_manager.game.start_run()
        self.screen_manager.change_screen("game", 20)