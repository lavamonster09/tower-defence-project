from misc.ui import *
from misc.constants import *
from screens.screen import Screen

class Settings(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (20,20,20)
        self.add_item("Title",Label(rect = (SCREEN_WIDTH/2 - 150,0,300,200),
                             text = "SETTINGS",
                             color = (0,0,0),
                             fore_color = (150,150,150)))
        self.add_item("Slider_1", Slider(pos = (SCREEN_WIDTH/2 - 150, 200),
                             length=400,
                             min_val=0,
                             max_val=100,
                             dot_size=10,
                             thickness=5,
                             line_color=(100,100,100),
                             dot_color=(200,200,200)))
        self.add_item("slider_1_label", Label(rect = (SCREEN_WIDTH/2 - 150, 200, 400, 50),
                             text = "Slider 1",
                             color = (0,0,0),
                             fore_color = (150,150,150)))
        self.add_item("slider_1_label_2", Label(rect = (SCREEN_WIDTH/2 - 275, 200 - 25, 100, 50),
                             text = "Volume:",
                             color = (0,0,0),
                             fore_color = (150,150,150)))       
        self.add_item("btn_back", Button(rect = (0,0,50,50),
                             fore_color = (200,200,200),
                             text = "X",
                             filled = False,
                             on_click= self.btn_back_on_click))
        self.add_item("dropdown", Dropdown(rect = (SCREEN_WIDTH/2 - 150, 250, 40, 50),
                                options = ["2560 x 1440","1920 x 1080", "1600 x 900", "1280 x 720"],
                                border_radius = 10,
                                border_width = 2,
                                color= (20,20,20),
                                border_color = (150,150,150),
                                fore_color = (200,200,200),
                                hover_color = (50, 50, 50)))
        self.add_item("dropdown_label", Label(rect = (SCREEN_WIDTH/2 - 275, 250, 100, 50),
                             text = "Resolution:",
                             color = (0,0,0),
                             fore_color = (150,150,150)))
    def update(self):
        super().update()
        self.items["slider_1_label"].text = str(f'{int(self.items["Slider_1"].value)} %')
        
    def btn_back_on_click(self):
        self.screen_manager.current_screen = "menu"