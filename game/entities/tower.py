from game.entities.entity import *
from misc.constants import *
from misc.util import *
import pygame
import math

class Tower(Entity):
    def __init__(self,entity_manager, position, sprite):
        super().__init__(entity_manager, position=position, sprite=sprite)
        self.range = 100
        self.bullet = None
        self.damage = 10
        self.can_shoot = True
        self.shoot_delay = 10
        self.shoot_cooldown = 0
        self.rotation = 0
        self.target = None
        self.hovered = False
        self.held = False
        self.velocity = pygame.Vector2(0,0)
        self.player_inrange = False

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1 
            self.can_shoot = False
        else:
            self.can_shoot = True
        self.pos += self.velocity
        self.velocity /= 1.05
        if "enemy" in self.entity_manager.entities:
            for enemy in self.entity_manager.entities["enemy"]:
                if (enemy.pos - self.pos).magnitude() < self.range:
                    if self.can_shoot:
                        self.rotation = self.get_rotation(enemy.pos)
                        enemy.hp -= self.damage
                        self.shoot_cooldown = self.shoot_delay
        super().update()
        
    def draw(self, target_surface):
        temp_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        self.rect = temp_sprite.get_rect()
        temp_sprite.set_colorkey((0,0,0))
        self.rect.center = self.pos
        target_surface.blit(temp_sprite, self.rect)
        if self.hovered:
            if self.player_inrange:
                pygame.draw.rect(target_surface, (255,255,255), self.rect, 2, 2)
            else:
                pygame.draw.rect(target_surface, (255,50,50), self.rect, 2, 2)
            pygame.draw.circle(target_surface, (255,255,255), self.rect.center, self.range, 2)
        if self.held:
            pygame.draw.circle(target_surface, (255,255,255), self.rect.center, self.range, 2)

    def get_rotation(self, target):
        target
        o = target.y - self.pos.y 
        a = target.x - self.pos.x
        deg = math.degrees(math.atan((o)/(a))) - 90
        if target.x < self.pos.x:
            angle = -deg
        else:
            angle = 180 - deg
        return angle