from misc.ui import *
from misc.theme import *
from screens.screen import Screen

class Settings(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (20,20,20)
        
        # Title
        self.add_item("Title", Label(LABEL_DARK, rect = (SCREEN_WIDTH/2 - 150,0,300,200), text = "SETTINGS"))

        # Slider_1
        self.add_item("Slider_1", Slider(SLIDER_DARK, pos = (SCREEN_WIDTH/2 - 150, 200), length = 400, min_val = 0, max_val = 100))
        self.add_item("slider_1_label", Label(LABEL_DARK, rect = (SCREEN_WIDTH/2 - 150, 200, 400, 50),text = "Slider 1"))
        self.add_item("slider_1_label_2", Label(LABEL_DARK, rect = (SCREEN_WIDTH/2 - 275, 200 - 25, 100, 50), text = "Volume:"))  

        # btn_back
        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (0,0,50,50), text = "X", on_click= self.btn_back_on_click))
        
        # Dropdown
        self.add_item("dropdown", Dropdown(DROPDOWN_DARK, rect = (SCREEN_WIDTH/2 - 150, 250, 400, 50), options = ["1280 x 720", "2560 x 1440","1920 x 1080", "1600 x 900"]))
        self.add_item("dropdown_label", Label(LABEL_DARK, rect = (SCREEN_WIDTH/2 - 275, 250, 100, 50),text = "Resolution:"))

    def update(self):
        super().update()
        display_width, display_height = self.items["dropdown"].get_selected_option().split(" x ")
        display_width, display_height = int(display_width), int(display_height)
        if [display_width, display_height] != [pygame.display.Info().current_w, pygame.display.Info().current_h]:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"name": "update_resolution", "resolution": [display_width, display_height]}))
        self.items["slider_1_label"].text = str(f'{int(self.items["Slider_1"].value)} %')
        
    def btn_back_on_click(self):
        self.screen_manager.current_screen = "menu"