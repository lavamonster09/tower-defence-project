import pygame
import pygame.gfxdraw
from engine.ui import *

class Screen():
    def __init__(self, screen_manager) -> None:
        self.items = {}  # Dictionary to store UI items
        self.animations = {}  # Dictionary to store animations
        self.screen_manager = screen_manager  
        self.screen = pygame.display.get_surface()  
        self.back_color = (0, 0, 0)  # Background color
        self.cursor_rad = 10  # Cursor radius
    
    def draw(self):
        # Fill the screen with the background color if it's not black
        if self.back_color != (0, 0, 0):
            self.screen.fill(self.back_color)
        
        # Draw all items
        for item in self.items:
            self.items[item].draw()
        
        # Adjust cursor appearance based on its type
        if pygame.mouse.get_cursor()[0] == pygame.SYSTEM_CURSOR_ARROW:
            if self.cursor_rad < 10:
                self.cursor_rad += 1
        if pygame.mouse.get_cursor()[0] == pygame.SYSTEM_CURSOR_HAND:
            if self.cursor_rad > 5:
                self.cursor_rad -= 1
        
        # Draw a circle around the cursor
        pygame.draw.circle(self.screen, (255, 255, 255), (int(pygame.mouse.get_pos()[0]), int(pygame.mouse.get_pos()[1])), self.cursor_rad, 3)

    def update(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Set default cursor
        # Update animations
        for animation in self.animations:
            if self.animations[animation][2] == "rect":
                updated = self.animations[animation][0].update()
                if updated: 
                    self.animations[animation][1].rect = pygame.Rect(updated)
        
        # Update all items
        for item in self.items.copy():
            if item in self.items:
                self.items[item].update()
            
    def add_item(self, name, item):
        # Add a new item to the screen
        self.items.update({name: item})

    def remove_item(self, name):
        # Remove an item from the screen
        if name in self.items:
            self.items.pop(name)

    def add_animation(self, name, start, end, length, target, target_type):
        # Add a new animation
        animation = Animation(start, end, length)
        self.animations.update({name: [animation, target, target_type]})
    
    def on_open(self):
        pass

    def on_close(self):
        return True