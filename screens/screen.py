import pygame
from misc.ui import *

class Screen():
    def __init__(self, screen_manager) -> None:
        self.items = []
        self.screen_manager = screen_manager
        self.screen = pygame.display.get_surface()
        self.back_color = (0,0,0)
    
    def draw(self):
        self.screen.fill(self.back_color)
        for item in self.items:
            item.draw()

    def update(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for item in self.items:
            item.update()
    
    def add_item(self, item):
        self.items.append(item)