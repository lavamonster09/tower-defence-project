from engine import *
from game.util.constants import *
import json 
import requests

class Leaderboard(Screen):
    def __init__(self, screen_manager) -> None:
        super().__init__(screen_manager)
        self.back_color = (DARK_BACKGROUND_COLOR)
            
        self.add_item("Title", Label(LABEL_DARK, rect = (50,10,SCREEN_WIDTH,200), text = "LEADERBOARD", positioning="relative", font_size=100)) 
        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("arrow_back"), on_click= self.btn_back_on_click))
        self.add_item("lbl_highscores", Label(LABEL_DARK, rect=(50,50,SCREEN_WIDTH/2,SCREEN_HEIGHT-50),text="",positioning="relative",font_size=30))

        self.add_item("btn_load", Button(BUTTON_DARK, rect=(50,90,180,100), text="refresh", on_click=self.on_open, positioning="relative"))

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.btn_back_on_click()
        return super().update()

    def btn_back_on_click(self):
        self.screen_manager.change_screen(self.screen_manager.before_last_screen, 20)

    def on_open(self):
        self.items["lbl_highscores"].text = ""
        try: 
            response = requests.get("http://127.0.0.1:5000/TEST", timeout=5)
        except (requests.Timeout, requests.ConnectionError):
            self.items["lbl_highscores"].text = "connection to server failed"
            return
        scores = []
        
        for i in range(len(response.json()["names"])):
            scores.append([response.json()["names"][i],response.json()["scores"][i]])
        scores.sort(key=lambda x: int(x[1]), reverse=True)
        for i in range(15):
            if i < len(scores):
                self.items["lbl_highscores"].text += f'{scores[i][0]} - {scores[i][1]} \n'