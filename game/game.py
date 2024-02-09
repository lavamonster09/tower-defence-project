from misc.ui import *
from misc.theme import *
from misc.constants import *
from screens.screen import Screen
import game.level as level
import pygame

class Game(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.level_manager = level.Level_manager(1.6)
    
    def draw(self):
        super().draw()
        self.level_manager.draw()
        self.screen.blit(pygame.transform.scale(self.level_manager.game_surf,( SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))