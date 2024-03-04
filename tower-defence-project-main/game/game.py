from misc.ui import *
from misc.theme import *
from misc.constants import *
from screens.screen import Screen
import game.level as level
import pygame

class Game(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.screen.set_colorkey((0,0,0))
        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("arrow_back"), on_click= self.btn_back_on_click))
        self.add_item("btn_generate", Button(BUTTON_DARK_NO_FILL , rect = (75,25,50,50), text = get_icon_hex("g_mobiledata"), on_click= self.btn_generate_on_click))
        self.level_manager = level.Level_manager(1.6)
        self.i = 0
    
    def draw(self):
        self.level_manager.draw()
        self.screen.blit(pygame.transform.scale(self.level_manager.game_surf,( SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        super().draw()
    
    def btn_back_on_click(self):
        self.screen_manager.change_screen(self.screen_manager.before_last_screen, 20)
        
    def btn_generate_on_click(self):
        self.level_manager.change_level(6,10)