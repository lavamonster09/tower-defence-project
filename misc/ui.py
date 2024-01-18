import pygame 
import math
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
        self.line_color = line_color
        self.dot_color = dot_color
        self.value = min_val
        self.screen = pygame.display.get_surface()
        self.sliding = False
    def draw(self):
        pygame.draw.line(self.screen, self.line_color, self.pos, self.pos + pygame.Vector2(self.length,0), self.thickness)
        pygame.draw.circle(self.screen, self.dot_color, self.pos + pygame.Vector2(self.length * (self.value - self.min_val)/(self.max_val - self.min_val), 0), self.dot_size)
    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if self.pos.y - self.dot_size <= pygame.mouse.get_pos()[1] <= self.pos.y + self.dot_size:
                self.sliding = True
        else:
            self.sliding = False
        if self.sliding:
            if self.pos.x <= pygame.mouse.get_pos()[0] <= self.pos.x + self.length:
                self.value = self.min_val + (self.max_val - self.min_val) * (pygame.mouse.get_pos()[0] - self.pos.x) / self.length
                if self.value > self.max_val: self.value = self.max_val
                if self.value < self.min_val: self.value = self.min_val
            elif pygame.mouse.get_pos()[0] < self.pos.x:
                self.value = self.min_val
            elif pygame.mouse.get_pos()[0] > self.pos.x + self.length:
                self.value = self.max_val

class Dropdown():
    def __init__(self, rect = (0,0,0,0), text = "", color = (0,0,0), border_radius=0, border_width=0, border_color = (0,0,0), hover_color = (0,0,0), fore_color = (0,0,0), filled = True, options = []):
        self.time = 1
        self.rect = pygame.Rect(rect[0], rect[1] , rect[2], rect[3])
        self.font = pygame.font.SysFont(MAIN_FONT, int(self.rect.height/2))
        self.options = options
        self.filled = filled
        self.text = text
        self.color = color
        self.fore_color = fore_color
        self.hover_color = hover_color
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color
        self.hovering = False
        self.lastpressed = False
        self.toggle = False
        self.hovered = None
        self.selected = None 
        self.screen = pygame.display.get_surface()

    def draw(self):
        if self.toggle:
            self.dropdown()
        if self.hovered != None:
            self.text = self.options[self.hovered]
            pygame.draw.rect(self.screen, self.hover_color, self.rect, border_radius= self.border_radius)
            if self.hovering:
                temp_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height * (self.hovered+1), self.rect.width, self.rect.height)
                pygame.draw.rect(self.screen, self.border_color, temp_rect, self.border_width, self.border_radius)
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
        if self.toggle:
            temp_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * (len(self.options)))
            if temp_rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                self.hovering = True
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.hovered = int((pygame.mouse.get_pos()[1] - self.rect.y - self.rect.height)/self.rect.height)
                if pygame.mouse.get_pressed()[0]:
                    self.selected = int((pygame.mouse.get_pos()[1] - self.rect.y - self.rect.height)/self.rect.height)
                    self.toggle = False
                    self.time = 1
            else:
                if pygame.mouse.get_pressed()[0]:
                    if pygame.mouse.get_pos()[0] < self.rect.x or pygame.mouse.get_pos()[0] > self.rect.x + self.rect.width or pygame.mouse.get_pos()[1] < self.rect.y or pygame.mouse.get_pos()[1] > self.rect.y + self.rect.height * (len(self.options) + 1):
                        self.toggle = False
                        self.time = 1
                self.hovering = False
        elif self.rect.x <= pygame.mouse.get_pos()[0] <= self.rect.x + self.rect.width and self.rect.y <= pygame.mouse.get_pos()[1] <= self.rect.y + self.rect.height:
            self.hovering = True
            self.hovered = None
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] and not self.lastpressed:
                self.lastpressed = True
                self.toggle = not self.toggle
        else:
            self.hovering = False
            self.lastpressed = False
    
    def dropdown(self):
        if self.time != 100: self.time += 10
        if self.time > 100: self.time = 100
        temp_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, (self.rect.height * (len(self.options) + 1)) * self.time / 100)
        pygame.draw.rect(self.screen, self.color, temp_rect, border_radius= self.border_radius)
        pygame.draw.rect(self.screen, self.border_color, temp_rect, border_radius= self.border_radius, width= self.border_width)
        for i, option in enumerate(self.options):
            if ((self.rect.height * (len(self.options) + 1)) * self.time / 100) // self.rect.height - 1 < i:
                continue
            temp_rect = pygame.Rect(self.rect.x + self.border_width , self.rect.y + self.rect.height * (i+1), self.rect.width - self.border_width * 2, self.rect.height - self.border_width)
            text_surf = self.font.render(option, True, self.fore_color)
            position = (temp_rect.x + (temp_rect.width - text_surf.get_width()) / 2, temp_rect.y + (temp_rect.height - text_surf.get_height()) / 2)
            self.screen.blit(text_surf, position)
