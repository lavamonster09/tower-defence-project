from game.entities.entity import *
from misc.constants import *
from misc.util import *
import pygame
import math

class Tower(Entity):
    def __init__(self, position, sprite):
        super().__init__(position=position, sprite=sprite)
        self.range = 0 
        self.bullet = None
        self.rotation = 0
        self.target = None
        self.hovered = False
        self.velocity = pygame.Vector2(0,0)
        self.player_inrange = False

    def update(self):
        self.pos += self.velocity
        self.velocity /= 1.05
        super().update()
        


    def draw(self, target_surface):
        super().draw(target_surface)
        if self.hovered:
            if self.player_inrange:
                pygame.draw.rect(target_surface, (255,255,255), self.rect, 2, 2)
            else:
                pygame.draw.rect(target_surface, (255,50,50), self.rect, 2, 2)
