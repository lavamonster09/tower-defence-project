from misc.ui import *
from misc.theme import *
from misc.constants import *
from screens.screen import Screen
import game.level as level
import pygame

class Game(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)

        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("arrow_back"), on_click= self.btn_back_on_click))
        self.add_item("btn_generate", Button(BUTTON_DARK_NO_FILL , rect = (75,25,50,50), text = get_icon_hex("replay"), on_click= self.btn_generate_on_click))

        self.add_item("sld_noturns", Slider(SLIDER_DARK, pos = (25, 75), length = 100, min_val = 1, max_val = 15))
        self.add_item("lbl_noturns", Label(LABEL_DARK, rect = (75, 100, 125, 50), text = "No. turns: 1", font_size=20))
        self.no_turns = 1

        self.add_item("sld_noboxes", Slider(SLIDER_DARK, pos = (25, 125), length = 100, min_val = 0, max_val = 5))
        self.add_item("lbl_noboxes", Label(LABEL_DARK, rect = (75, 150, 125, 50), text = "No. boxes: 1", font_size=20))
        self.no_boxes = 1

        self.add_item("sld_maxlinelen", Slider(SLIDER_DARK, pos = (25, 175), length = 100, min_val = 300, max_val = 1200))
        self.add_item("lbl_maxlinelen", Label(LABEL_DARK, rect = (75, 200, 125, 50), text = "Max line len: 100", font_size=20))
        self.max_line_len = 300
        
        self.level_manager = level.Level_manager(1.6)
    
    def draw(self):
        self.level_manager.draw()
        self.screen.blit(pygame.transform.scale(self.level_manager.game_surf,( SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        super().draw()
    
    def update(self):
        super().update()
        if int(self.items["sld_noturns"].value) != self.no_turns:
            self.items["lbl_noturns"].text = f"No. turns: {int(self.items['sld_noturns'].value)}"
            self.no_turns = int(self.items["sld_noturns"].value)
            self.level_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
        if int(self.items["sld_noboxes"].value) != self.no_boxes:
            self.items["lbl_noboxes"].text = f"No. boxes: {int(self.items['sld_noboxes'].value)}"
            self.no_boxes = int(self.items["sld_noboxes"].value)
            self.level_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
        if int(self.items["sld_maxlinelen"].value) != self.max_line_len:
            self.items["lbl_maxlinelen"].text = f"Max line len: {int(self.items['sld_maxlinelen'].value)}"
            self.max_line_len = int(self.items["sld_maxlinelen"].value)
            self.level_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
    
    def btn_back_on_click(self):
        self.screen_manager.change_screen(self.screen_manager.before_last_screen, 20)
        
    def btn_generate_on_click(self):
        self.level_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)