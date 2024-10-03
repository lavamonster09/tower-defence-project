from engine import *
from util.constants import *

class Upgrades(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (DARK_BACKGROUND_COLOR)

        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("arrow_back"), on_click= self.btn_back_on_click))

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.btn_back_on_click()
        return super().update()

    def btn_back_on_click(self):
        self.screen_manager.change_screen(self.screen_manager.before_last_screen, 20)