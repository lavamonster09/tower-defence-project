from game.entities.entity import *
from misc.constants import *
from misc.util import *
import pygame
import math

class Player(Entity):
    def __init__(self,entity_manager, sprite = pygame.surface.Surface((0,0)), speed = 0.75) -> None:
        super().__init__(position = pygame.Vector2(0,0), sprite = sprite)
        self.speed = speed
        self.velocity = pygame.Vector2(0,0)
        self.entity_manager = entity_manager
        self.m_last_pressed = pygame.mouse.get_pressed()
        self.k_last_pressed = pygame.key.get_pressed()
        self.holding = None
        self.target_angle = 0
        self.angle = 0
    
    def update(self):
        super().update()
        self.target_angle = self.get_rotation()
        self.angle += (self.target_angle - self.angle) / 10
        m_pressed = pygame.mouse.get_pressed()
        k_pressed = pygame.key.get_pressed()
        self.move()
        for tower in self.entity_manager.entities["tower"]:
            x_inrange = in_range(pygame.mouse.get_pos()[0] / SCREEN_SCALE, [tower.rect.x, tower.rect.x + tower.rect.width])
            y_inrange = in_range(pygame.mouse.get_pos()[1] / SCREEN_SCALE, [tower.rect.y, tower.rect.y + tower.rect.height])
            if tower != self.holding:
                if (tower.pos - self.pos).magnitude() <= 75:
                    tower.player_inrange = True
                    if x_inrange and y_inrange:
                        tower.hovered = True
                        if m_pressed[0] == True and self.m_last_pressed[0] == False:
                            self.m_last_pressed = m_pressed
                            self.holding = tower
                else:
                    tower.player_inrange = False
                if x_inrange and y_inrange:
                    tower.hovered = True
                else:
                    tower.hovered = False
            else:
                tower.player_inrange = False
                tower.hovered = False
                if m_pressed[0] == True and self.m_last_pressed[0] == False:
                    self.holding = None
                if m_pressed[2] == True and self.m_last_pressed[2] == False:
                    self.holding.velocity =( pygame.Vector2(0,-7).rotate(-self.angle)) + self.velocity * 1.5
                    self.holding = None
        self.m_last_pressed = m_pressed
        self.k_last_pressed = k_pressed
        if self.holding != None:
            self.holding.pos = self.pos + pygame.Vector2(0,-32).rotate(-self.angle)

    def move(self):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0,0)
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_d]:
            direction.x += 1 
        
        if not direction == pygame.Vector2(0,0):
            direction = direction.normalize()    
        
        self.velocity /= 1.2
         
        
        self.velocity += self.speed * direction
        self.pos += self.velocity
        
    def draw(self, target_surface):
        temp_sprite = pygame.transform.rotate(self.sprite, self.target_angle)
        self.rect = temp_sprite.get_rect()
        temp_sprite.set_colorkey((0,0,0))
        self.rect.center = self.pos
        temp_sprite
        target_surface.blit(temp_sprite, self.rect)
    
    def get_rotation(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) / SCREEN_SCALE
        o = mouse_pos.y - self.pos.y 
        a = mouse_pos.x - self.pos.x
        deg = math.degrees(math.atan((o)/(a))) - 90
        if mouse_pos.x < self.pos.x:
            angle = -deg
        else:
            angle = 180 - deg
        return angle