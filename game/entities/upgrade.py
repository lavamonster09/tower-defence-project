from game.entities.entity import *
from misc.constants import *
from misc.util import *
import pygame
import math

class Upgrade(Entity):
    def __init__(self,game_manager, position, sprite):
        super().__init__(game_manager, position=position, sprite=sprite)

        self.pickup_rect = self.rect
        self.velocity = pygame.Vector2(0,0)

        self.hovered = False
        self.held = False
        self.player_inrange = False
        self.holdable = True

    def update(self):
        if self.check_collisions() or self.pos.x > SCREEN_WIDTH or self.pos.x < 0 or self.pos.y > SCREEN_HEIGHT or self.pos.y < 0:
            self.velocity *= -1
        self.pos += self.velocity
        self.velocity /= 1.05
        super().update()

    def draw(self, target_surface):
        target_surface.blit(self.sprite, self.rect)
        if self.hovered:
            self.pickup_rect.center = self.pos
            if self.player_inrange:
                pygame.draw.rect(target_surface, (255,255,255), self.pickup_rect, 3, 2)
            else:
                pygame.draw.rect(target_surface, (255,50,50), self.pickup_rect, 3, 2)

    def check_collisions(self):
        for obsticle in self.level_manager.current_level.obsticles:
            if obsticle.collidepoint(self.pos):
                return True
        return False