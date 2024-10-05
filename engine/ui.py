import pygame 
from pygame import gfxdraw
import math
from engine.theme import *
from util.constants import *
from typing import Callable

pygame.font.init()

d = {}
with open("assets/fonts/MaterialIcons-Regular.codepoints", "r") as file:
    for line in file:
        (key, val) = line.split()
        d[key] = val

def get_icon_hex(icon):
    return chr(int(f"0x{d[icon]}",0))

class Button():
    def __init__(self, theme:Theme, rect = (0,0,0,0), text = "", on_click = None, click_args = [], positioning = "absolute"):
        # passed in button variable
        self.rect = pygame.Rect(0, 0 , rect[2], rect[3])
        if positioning == "absolute":
            self.rect.center = (rect[0], rect[1])
        if positioning == "relative":
            self.rect.center = ((rect[0] / 100) * SCREEN_WIDTH, (rect[1] / 100) * SCREEN_HEIGHT)      
        self.text = text
        self.on_click = on_click

        # button specific needed variables
        self.click_args = click_args
        self.font = pygame.font.Font(MAIN_FONT, int(self.rect.height/2))
        self.icon_font = pygame.font.Font(ICON_FONT, int(self.rect.height/2))
        self.icon_font.set_bold(True)
        self.hovering = False
        self.hidden = False
        if pygame.mouse.get_pressed()[0]:
            self.lastpressed = True
        else:
            self.lastpressed = False

        # theme
        self.filled = theme.get()["filled"]
        self.color = theme.get()["color"]
        self.fore_color = theme.get()["fore_color"]
        self.hover_color = theme.get()["hover_color"]
        self.border_radius = theme.get()["border_radius"]
        self.border_width = theme.get()["border_width"]
        self.border_color = theme.get()["border_color"]

        # globaly needed variables
        self.screen = pygame.display.get_surface()
    
    def draw(self):
        if self.hidden:
            return
        # check if button is filled and if it is hovering
        if self.filled and self.hovering:
            pygame.draw.rect(self.screen, self.hover_color, self.rect, border_radius= self.border_radius)
        elif self.filled:
            pygame.draw.rect(self.screen, self.color, self.rect, border_radius= self.border_radius)

        # check if button has a border
        if self.border_width > 0: pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_width, self.border_radius)   

        # draw text
        if self.text.isalpha() or self.text.isnumeric():
            text_surf = self.font.render(self.text, True, self.fore_color)
            position = (self.rect.x + (self.rect.width - text_surf.get_width()) / 2, self.rect.y + (self.rect.height - text_surf.get_height()) / 2)
            self.screen.blit(text_surf, position)
        else:
            text_surf = self.icon_font.render(self.text, True, self.fore_color)
            position = (self.rect.x + (self.rect.width - text_surf.get_width()) / 2, self.rect.y + (self.rect.height - text_surf.get_height()) / 2)
            self.screen.blit(text_surf, position)
    
    def update(self):
        if self.hidden:
            return
        # check if mouse is hovering over button
        if self.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
            self.hovering = True
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

            # check if mouse is clicking on button
            if pygame.mouse.get_pressed()[0]:
                if self.on_click and not self.lastpressed: 
                    self.lastpressed = True
                    self.on_click(*self.click_args)
            else:
                self.lastpressed = False
        else:
            if pygame.mouse.get_pressed()[0]:
                self.lastpressed = True
            else:
                self.lastpressed = False
            self.hovering = False

class Label():
    def __init__(self, theme:Theme, rect = (0,0,0,0), text = "", positioning = "absolute", font_size = 0):
        # passed in label variables
        self.function = None
        self.rect = pygame.Rect(0, 0 , rect[2], rect[3])
        if positioning == "absolute":
            self.rect.center = (rect[0], rect[1])
        if positioning == "relative":
            self.rect.center = ((rect[0] / 100) * SCREEN_WIDTH, (rect[1] / 100) * SCREEN_HEIGHT)      
        self.font = pygame.font.Font(MAIN_FONT, font_size)
        if isinstance(text, Callable):
            self.text = str(text())
            self.function = text
        else:
            self.text = text

        # theme
        self.filled = theme.get()["filled"]
        self.color  = theme.get()["color"]
        self.fore_color = theme.get()["fore_color"]
        self.border_radius = theme.get()["border_radius"]
        self.border_width = theme.get()["border_width"]
        self.border_color = theme.get()["border_color"]

        # globaly needed variables
        self.screen = pygame.display.get_surface()

        self.hidden = False
    
    def draw(self):
        if self.hidden:
            return
        # check if label is filled
        if self.filled: pygame.draw.rect(self.screen, self.color, self.rect, border_radius= self.border_radius)
            
        # check if label has a border
        if self.border_width > 0: pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_width, self.border_radius)   
            
        # draw text
        text_surf = self.font.render(self.text, True, self.fore_color, wraplength=self.rect.width)
        position = (self.rect.x + (self.rect.width - text_surf.get_width()) / 2, self.rect.y + (self.rect.height - text_surf.get_height()) / 2)
        self.screen.blit(text_surf, position)
    
    def update(self):
        if self.function:
            self.text = self.function()
            if type(self.text) == int:
                self.text = str(self.text)
            elif type(self.text) == float:
                self.text = str(round(self.text, 2))
        if self.hidden:
            return
        pass

class Slider():
    def __init__(self,theme:Theme, pos= (0,0), length = 0,min_val = 0, max_val = 0) -> None:
        # passed in slider variables
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.min_val = min_val
        self.max_val = max_val
        self.length = length
        self.value = min_val
        
        # button specific needed variables
        self.sliding = False

        # theme
        self.thickness = theme.get()["thickness"]
        self.dot_size = theme.get()["dot_size"]
        self.line_color = theme.get()["line_color"]
        self.dot_color = theme.get()["dot_color"]

        # globaly needed variables
        self.screen = pygame.display.get_surface()

        self.hidden = False
        
    def draw(self):
        if self.hidden:
            return
        gfxdraw.filled_circle(self.screen,int(self.pos.x),int(self.pos.y), self.thickness // 2, self.line_color)
        gfxdraw.filled_circle(self.screen,int(self.pos.x + self.length),int(self.pos.y), self.thickness // 2, self.line_color)
        pygame.draw.line(self.screen, self.line_color, self.pos, self.pos + pygame.Vector2(self.length,0), self.thickness)
        gfxdraw.aacircle(self.screen,int(self.pos.x + self.length * (self.value - self.min_val)/(self.max_val - self.min_val)),int(self.pos.y), self.dot_size, self.dot_color)
        gfxdraw.filled_circle(self.screen,int(self.pos.x + self.length * (self.value - self.min_val)/(self.max_val - self.min_val)),int(self.pos.y), self.dot_size, self.dot_color)
        

    def update(self):
        if self.hidden:
            return
        #check if mouse is hovering over slider
        if self.pos.y - self.dot_size <= pygame.mouse.get_pos()[1] <= self.pos.y + self.dot_size and self.pos.x <= pygame.mouse.get_pos()[0] <= self.pos.x + self.length:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            
        #check if mouse is pressing on slider
        if pygame.mouse.get_pressed()[0]:
            if self.pos.y - self.dot_size <= pygame.mouse.get_pos()[1] <= self.pos.y + self.dot_size and self.pos.x <= pygame.mouse.get_pos()[0] <= self.pos.x + self.length:
                self.sliding = True
        else:
            self.sliding = False
        
        # check if slider is sliding
        if self.sliding:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if self.pos.x <= pygame.mouse.get_pos()[0] <= self.pos.x + self.length:
                self.value = self.min_val + (self.max_val - self.min_val) * (pygame.mouse.get_pos()[0] - self.pos.x) / self.length
                if self.value > self.max_val: self.value = self.max_val
                if self.value < self.min_val: self.value = self.min_val
            elif pygame.mouse.get_pos()[0] < self.pos.x:
                self.value = self.min_val
            elif pygame.mouse.get_pos()[0] > self.pos.x + self.length:
                self.value = self.max_val
    
class Dropdown():
    def __init__(self,theme:Theme, rect = (0,0,0,0), options = [], positioning = "absolute"):
        # passed in dropdown variables  
        self.rect = pygame.Rect(0, 0 , rect[2], rect[3])
        if positioning == "absolute":
            self.rect.center = (rect[0], rect[1])
        if positioning == "relative":
            self.rect.center = ((rect[0] / 100) * SCREEN_WIDTH, (rect[1] / 100) * SCREEN_HEIGHT)      
        self.options = options

        # dropdown specific needed variables
        self.font = pygame.font.Font(MAIN_FONT, int(self.rect.height/2))
        self.time = 1
        self.text = ""
        self.hovering = False
        self.lastpressed = False
        self.toggle = False
        self.hovered = None
        self.selected = None 

        # theme
        self.filled = theme.get()["filled"]
        self.color = theme.get()["color"]
        self.fore_color = theme.get()["fore_color"]
        self.hover_color = theme.get()["hover_color"]
        self.border_radius = theme.get()["border_radius"]
        self.border_width = theme.get()["border_width"]
        self.border_color = theme.get()["border_color"]
        
        # globaly needed variables
        self.screen = pygame.display.get_surface()

        self.hidden = False

    def draw(self):
        if self.hidden:
            return
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
        if self.hidden:
            return
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
        if self.border_width > 0:
            pygame.draw.rect(self.screen, self.border_color, temp_rect, border_radius= self.border_radius, width= self.border_width)
        for i, option in enumerate(self.options):
            if ((self.rect.height * (len(self.options) + 1)) * self.time / 100) // self.rect.height - 1 < i:
                continue
            temp_rect = pygame.Rect(self.rect.x + self.border_width , self.rect.y + self.rect.height * (i+1), self.rect.width - self.border_width * 2, self.rect.height - self.border_width)
            text_surf = self.font.render(option, True, self.fore_color)
            position = (temp_rect.x + (temp_rect.width - text_surf.get_width()) / 2, temp_rect.y + (temp_rect.height - text_surf.get_height()) / 2)
            self.screen.blit(text_surf, position)
    
    def get_selected_option(self):
        if self.selected != None:
            return self.options[self.selected]
        else:
            return self.options[0]

class Image():
    def __init__(self, image, rect = (0,0,0,0), positioning = "absolute"):
        self.rect = pygame.Rect(0, 0 , rect[2], rect[3])
        if positioning == "absolute":
            self.rect.center = (rect[0], rect[1])
        if positioning == "relative":
            self.rect.center = ((rect[0] / 100) * SCREEN_WIDTH, (rect[1] / 100) * SCREEN_HEIGHT)      
        if image != "":
            self.image = pygame.image.load(image).convert()
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            self.image.set_colorkey((0,0,0))
        else:
            self.image = ""
        self.screen = pygame.display.get_surface()
        self.hidden = False

    def draw(self):
        if self.hidden:
            return
        if self.image != "":
            self.screen.blit(self.image, self.rect)

    def update(self):
        if self.hidden:
            return
        pass

    def set_image(self, image):
        self.image = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.set_colorkey((0,0,0))

class Rect():
    def __init__(self, theme, rect, positioning = "absolute") -> None:
        #passed in variables
        self.rect = pygame.Rect(0, 0 , rect[2], rect[3])
        if positioning == "absolute":
            self.rect.center = (rect[0], rect[1])
        if positioning == "relative":
            self.rect.center = ((rect[0] / 100) * SCREEN_WIDTH, (rect[1] / 100) * SCREEN_HEIGHT)

        #from theme
        self.color = theme.get()["color"]
        self.border_radius = theme.get()["border_radius"]
        self.border_width = theme.get()["border_width"]
        self.border_color = theme.get()["border_color"]
        self.filled = theme.get()["filled"]

        #needed variables
        self.screen = pygame.display.get_surface()
        self.hidden = False
        
    
    def draw(self):
        if self.hidden:
            return
        if self.filled:
            pygame.draw.rect(self.screen, self.color, self.rect, border_radius= self.border_radius)
        if self.border_width > 0:
            pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_width, self.border_radius)
    
    def update(self):
        pass

class Amimation():
    def __init__(self, start, end, length):
        self.start = start
        self.end = end
        self.current = []
        self.frame = 0
        self.length = length
        self.animate = False

    def update(self):
        if self.animate:
            if self.frame > self.length:
                self.animate = False
                self.current = self.end
                return self.end
            else:
                for i in range(len(self.current)):
                    self.current[i] = self.start[i] + (self.end[i] - self.start[i]) * (math.sqrt(self.frame) / math.sqrt(self.length))
                self.frame += 1
                return self.current
        else:
            return False
    
    def start_animation(self):
        self.animate = True
        self.frame = 0
        self.current = [None for i in range(len(self.start))]
        for i in range(len(self.start)):
            self.current[i] = self.start[i]
        self.update()


class Popup():
    def __init__(self, game, elements = []) -> None:
        self.screen = pygame.display.get_surface()
        self.hidden = False
        self.elements = elements
        self.game = game
    
    def show(self):
        self.hidden = False
    
    def hide(self):
        self.hidden = True

    def add_item(self, item):
        self.elements.append(item)
    
    def draw(self):
        if self.hidden:
            return
        for element in self.elements:
            element.draw()
    
    def update(self):
        if self.hidden:
            return
        for element in self.elements:
            element.update()
    
    def on_close(self):
        pass