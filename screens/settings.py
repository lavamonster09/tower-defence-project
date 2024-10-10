from engine import *
from util.constants import *

class Settings(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (DARK_BACKGROUND_COLOR)
        
        # Dropdown
        self.add_item("dropdown", Dropdown(DROPDOWN_DARK, rect = (54, 40, 400, 50), options = ["1280 x 720", "2560 x 1440","1920 x 1080", "1600 x 900"], positioning="relative"))
        self.add_item("dropdown_label", Label(LABEL_DARK, rect = (SCREEN_WIDTH/2 - 275, 275, 400, 50),text = "Resolution:", font_size=30))
        
        # sldr_sfx
        self.add_item("sldr_sfx", Slider(SLIDER_DARK, pos = (SCREEN_WIDTH/2 - 150, 170), length = 400, min_val = 0, max_val = 100))
        self.add_item("sldr_sfx_label", Label(LABEL_DARK, rect = (54, 26, 400, 50),text = "Slider 1", positioning="relative", font_size=20))
        self.add_item("sldr_sfx_label_2", Label(LABEL_DARK, rect = (SCREEN_WIDTH/2 - 275, 200 - 25, 400, 50), text = "Volume:", font_size=30))
        self.items["sldr_sfx"].value = float(self.screen_manager.game.config["SOUND_VOLUME"]) * 100

        # sldr_music
        self.add_item("sldr_music", Slider(SLIDER_DARK, pos = (SCREEN_WIDTH/2 - 150, 225), length = 400, min_val = 0, max_val = 100))
        self.add_item("sldr_music_label", Label(LABEL_DARK, rect = (54, 34, 400, 50),text = "Slider 2", positioning="relative", font_size=20))
        self.add_item("sldr_music_label_2", Label(LABEL_DARK, rect = (SCREEN_WIDTH/2 - 275, 225, 400, 50), text = "Music Volume:", font_size=30))
        self.items["sldr_music"].value = float(self.screen_manager.game.config["MUSIC_VOLUME"]) * 100

        # btn_back
        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("arrow_back"), on_click= self.btn_back_on_click)) 

        # btn_save
        self.add_item("btn_save", Button(BUTTON_DARK , rect = (95,95,100,50), text = "save", positioning="relative", on_click= self.save_settings)) 

        # Title
        self.add_item("Title", Label(LABEL_DARK, rect = (50,10,SCREEN_WIDTH,200), text = "SETTINGS", positioning="relative", font_size=100)) 

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.btn_back_on_click()
        super().update()
        display_width, display_height = self.items["dropdown"].get_selected_option().split(" x ")
        display_width, display_height = int(display_width), int(display_height)
        if [display_width, display_height] != [pygame.display.Info().current_w, pygame.display.Info().current_h]:
            pygame.event.post(pygame.event.Event(RESOLUTION_UPDATE, {"resolution": [display_width, display_height]}))

        self.items["sldr_sfx_label"].text = str(f'{int(self.items["sldr_sfx"].value)} %')
        self.screen_manager.game.config["SOUND_VOLUME"] = self.items["sldr_sfx"].value / 100

        self.screen_manager.game.config["MUSIC_VOLUME"] = self.items["sldr_music"].value / 100
        self.items["sldr_music_label"].text = str(f'{int(self.items["sldr_music"].value)} %')
        pygame.mixer.music.set_volume(self.screen_manager.game.config.get("MUSIC_VOLUME"))
        
    def btn_back_on_click(self):
        self.screen_manager.change_screen(self.screen_manager.before_last_screen, 20)
 
    def save_settings(self):
        with open("config.cfg", "r") as fconfig:
            file = fconfig.readlines()
        with open("config.cfg", "w") as fconfig:
            for line in file:
                split = line.split(" ")
                if line[0] != "#" and len(split) > 1:
                    for setting in self.screen_manager.game.config:
                        if split[0].upper() == setting.upper():
                            fconfig.write(f"{split[0]} {self.screen_manager.game.config[setting]}")
                            fconfig.write("\n")
                    if split[0].upper() == "BIND":
                        for keybind in self.screen_manager.game.keybinds:
                            if split[2].strip("\n") == keybind:
                                key = pygame.key.name(self.screen_manager.game.keybinds[keybind])
                                fconfig.write(f"BIND {key} {keybind} \n")
                else:
                    fconfig.write(line)
