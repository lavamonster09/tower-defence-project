from engine import *
from game.util.constants import *

hero_data = {
    "tvman": {
        "name": "tvman",
        "small_image": "assets/images/heroes/tvman_small.png",
        "large_image": "assets/images/heroes/tvman_large.png",
        "description": "null"
    },
    "redman": {
        "name": "redman",
        "small_image": "assets/images/heroes/redman_small.png",
        "large_image": "assets/images/heroes/redman_large.png",
        "description": "red is angry the color suggest anger and rage. red is the hue of blood."
    },
    "purpleman": {
        "name": "purpleman",
        "small_image": "assets/images/heroes/purpleman_small.png",
        "large_image": "assets/images/heroes/purpleman_large.png",
        "description": "purple is a hue of blue and red. purple is a royal color. purple is a hue of violet."
    },
    "yellowman": {
        "name": "yellowman",
        "small_image": "assets/images/heroes/yellowman_small.png",
        "large_image": "assets/images/heroes/yellowman_large.png",
        "description": "yellow is the color of the sun. yellow is a hue of orange. yellow is a hue of green."
    },
    "pinkman": {
        "name": "pinkman",
        "small_image": "assets/images/heroes/pinkman_small.png",
        "large_image": "assets/images/heroes/pinkman_large.png",
        "description": "pink is a hue of red. pink is a hue of purple. pink is a hue of white."
    },
    "blueman": {
        "name": "blueman",
        "small_image": "assets/images/heroes/blueman_small.png",
        "large_image": "assets/images/heroes/blueman_large.png",
        "description": "blue is the color of the sky. blue is a hue of blue."
    }
}

class Heroes(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (DARK_BACKGROUND_COLOR)

        self.heroes = hero_data
        for i, hero in enumerate(self.heroes):   
            self.add_item(f"{hero}_img", Image(self.heroes[hero]["small_image"], rect = (100+i % 5*110 ,100+i//5 * 110,100,100)))
            self.add_item(f"{hero}_btn", Button(BUTTON_DARK_NO_FILL, rect = (100+i % 5*110 ,100+i//5 * 110,100,100), on_click = self.btn_heroes_on_click))

        # cursors 
        self.add_item("hovering", Rect(RECT_DARK_NO_FILL, rect = (100,100,100,100)))
        self.add_item("selected", Rect(RECT_DARK_NO_FILL, rect = (100,100,100,100)))
        self.items["selected"].border_color = DARK_ACCENT_COLOR

        # large hero
        self.add_item("description", Label(LABEL_DARK_FILLED, rect = (75, 75, SCREEN_WIDTH/4, 100), text = "Description", positioning="relative", font_size=20))
        self.add_item("large_hero", Image("", rect = (75,40,SCREEN_WIDTH/5,SCREEN_HEIGHT/2.5), positioning="relative"))
        self.add_item("hero_name", Label(LABEL_DARK_FILLED, rect = (75,10,SCREEN_WIDTH/4,100), positioning="relative", font_size=50, text="Hero Name"))

        # btns
        self.add_item("btn_select", Button(BUTTON_DARK, rect = (25, 80, 270, 100), text = "SELECT", positioning="relative", on_click= self.btn_select_on_click))
        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("arrow_back"), on_click= self.btn_back_on_click))

        self.btn_heroes_on_click()

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.btn_back_on_click()
        return super().update()
        
    def btn_back_on_click(self):
        self.screen_manager.change_screen("game_select", 20)

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
        self.screen_manager.game.selected_hero = self.items["hero_name"].text 
        self.items["btn_select"].color = DARK_SURFACE_HOVER_COLOR
        self.items["btn_select"].text = "SELECTED"