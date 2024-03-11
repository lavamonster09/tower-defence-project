import pygame
from misc.ui import *

class Screen():
    def __init__(self, screen_manager) -> None:
        self.items = {}
        self.animations = {}
        self.screen_manager = screen_manager
        self.screen = pygame.display.get_surface()
        self.back_color = (0,0,0)
    
    def draw(self):
        if self.back_color != (0,0,0):
            self.screen.fill(self.back_color)
        for item in self.items:
            self.items[item].draw()

    def update(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for animation in self.animations:
            if self.animations[animation][2] == "rect":
                updated = self.animations[animation][0].update()
                if updated: self.animations[animation][1].rect = pygame.Rect(updated)
        for item in self.items:
            self.items[item].update()
            
    def add_item(self,name, item):
        self.items.update({name:item})

    def add_animation(self, name, start, end, length, target, target_type):
        animation = Amimation(start, end, length)
        self.animations.update({name:[animation, target, target_type]})
    
    def on_open(self):
        pass

    def on_close(self):
        return True