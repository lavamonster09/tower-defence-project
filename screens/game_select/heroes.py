from misc.ui import *
from misc.theme import *
from misc.constants import *
from screens.screen import Screen

import json

class Heroes(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (DARK_BACKGROUND_COLOR)

        self.heroes = json.load(open("screens\game_select\heroes.json"))
        for i, hero in enumerate(self.heroes):   
            self.add_item(f"{hero}_img", Image(self.heroes[hero]["small_image"], rect = (75+i % 5*110 ,100+i//5 * 110,100,100)))
            self.add_item(f"{hero}_btn", Button(BUTTON_DARK_NO_FILL, rect = (75+i % 5*110 ,100+i//5 * 110,100,100), on_click = self.btn_heroes_on_click))

        # cursors 
        self.add_item("hovering", Rect(RECT_DARK_NO_FILL, rect = (75,100,100,100)))
        self.add_item("selected", Rect(RECT_DARK_NO_FILL, rect = (75,100,100,100)))
        self.items["selected"].border_color = DARK_ACCENT_COLOR

        # large hero
        self.add_item("description", Label(LABEL_DARK_FILLED, rect = (75, 75, SCREEN_WIDTH/4, 100), text = "Description", positioning="relative", font_size=20))
        self.add_item("large_hero", Image("", rect = (75,40,SCREEN_WIDTH/5,SCREEN_HEIGHT/2.5), positioning="relative"))
        self.add_item("hero_name", Label(LABEL_DARK_FILLED, rect = (75,10,SCREEN_WIDTH/4,100), positioning="relative", font_size=50, text="Hero Name"))

        # btns
        self.add_item("btn_select", Button(BUTTON_DARK, rect = (25, 80, 270, 100), text = "SELECT", positioning="relative", on_click= self.btn_select_on_click))
        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = "X", on_click= self.btn_back_on_click))

    def btn_back_on_click(self):
        self.screen_manager.current_screen = "game_select"

    def btn_heroes_on_click(self):
        for hero in self.heroes:
            if self.items[f"{hero}_btn"].lastpressed:
                self.items["hovering"].rect = self.items[f"{hero}_img"].rect
                self.items["hero_name"].text = hero
                self.items["description"].text = self.heroes[self.items["hero_name"].text]["description"]
                self.items["large_hero"].set_image(self.heroes[hero]["large_image"])
            if self.items["selected"].rect == self.items["hovering"].rect:
                self.items["btn_select"].text = "SELECTED"
                self.items["btn_select"].color = DARK_SURFACE_HOVER_COLOR
            else:
                self.items["btn_select"].text = "SELECT"
                self.items["btn_select"].color = DARK_SURFACE_LOW_COLOR
    
    def btn_select_on_click(self):
        self.items["selected"].rect = self.items["hovering"].rect
        self.items["btn_select"].color = DARK_SURFACE_HOVER_COLOR
        self.items["btn_select"].text = "SELECTED"