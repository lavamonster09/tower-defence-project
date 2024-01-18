import pygame 
from misc.constants import *

class Button():
    def __init__(self, rect = (0,0,0,0), text = "", color = (0,0,0), border_radius=0, border_width=0, border_color = (0,0,0), hover_color = (0,0,0), on_click = None, fore_color = (0,0,0), filled = True):
        self.rect = pygame.Rect(rect[0], rect[1] , rect[2], rect[3])
        self.font = pygame.font.SysFont(MAIN_FONT, int(self.rect.height/2))
        self.filled = filled
        self.text = text
        self.color = color
        self.fore_color = fore_color
        self.hover_color = hover_color
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color
        self.screen = pygame.display.get_surface()
        self.on_click = on_click
        self.hovering = False
        self.lastpressed = False
    
    def draw(self):
        if self.filled:
            if self.hovering:
                pygame.draw.rect(self.screen, self.hover_color, self.rect, border_radius= self.border_radius)
            else:
                pygame.draw.rect(self.screen, self.color, self.rect, border_radius= self.border_radius)
        if self.border_width > 0:
            pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_width, self.border_radius)   

        text_surf = self.font.render(self.text, True, self.fore_color)
        position = (self.rect.x + (self.rect.width - text_surf.get_width()) / 2, self.rect.y + (self.rect.height - text_surf.get_height()) / 2)
        self.screen.blit(text_surf, position)
    
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
            self.hovering = True
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0]:
                if self.on_click and not self.lastpressed: self.on_click()
                self.lastpressed = True
            else:
                self.lastpressed = False
        else:
            self.hovering = False

class Label():
    def __init__(self, rect, text, color, border_radius=0, border_width=0, border_color = (0,0,0), fore_color = (0,0,0), filled = False):
        self.rect = pygame.Rect(rect[0], rect[1] , rect[2], rect[3])
        self.filled = filled
        self.font = pygame.font.SysFont(MAIN_FONT, int(self.rect.height/2))
        self.text = text
        self.color = color
        self.fore_color = fore_color
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color
        self.screen = pygame.display.get_surface()
    
    def draw(self):
        if self.filled:
            pygame.draw.rect(self.screen, self.color, self.rect, border_radius= self.border_radius)
            
        if self.border_width > 0:
            pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_width, self.border_radius)   

        text_surf = self.font.render(self.text, True, self.fore_color)
        position = (self.rect.x + (self.rect.width - text_surf.get_width()) / 2, self.rect.y + (self.rect.height - text_surf.get_height()) / 2)
        self.screen.blit(text_surf, position)
    
    def update(self):
        pass

class Slider():
    def __init__(self, pos= (0,0), length = 0,min_val = 0, max_val = 0, dot_size = 2, thickness = 1, line_color = (0,0,0), dot_color = (0,0,0)) -> None:
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.min_val = min_val
        self.max_val = max_val
        self.thickness = thickness
        self.length = length
        self.dot_size = dot_size