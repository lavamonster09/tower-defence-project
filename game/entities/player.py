from game.entities.entity import *
from misc.constants import *
from misc.util import *
import pygame
import math

class Player(Entity):
    def __init__(self,game_manager, sprite = pygame.surface.Surface((0,0)), speed = 1.4) -> None:
        super().__init__(game_manager, position = pygame.Vector2(0,0), sprite = sprite)
        self.speed = speed
        self.velocity = pygame.Vector2(0,0)
        self.m_last_pressed = pygame.mouse.get_pressed()
        self.k_last_pressed = pygame.key.get_pressed()
        self.holding = None
        self.target_angle = 0
        self.angle = 0
    
    def update(self):
        super().update()
        self.target_angle = self.get_rotation()
        
        if self.angle > 360 or self.angle < 0:
            self.angle %= 360

        if (self.target_angle + 360 - self.angle) / 10 < (self.angle - self.target_angle) / 10:
            self.angle += abs((self.target_angle + 360 - self.angle) // 10)
        elif (self.target_angle - self.angle) / 10 > (self.angle + 360 - self.target_angle) / 10:
            self.angle -= abs((self.angle + 360 - self.target_angle) // 10)
        else:
            self.angle -= (self.angle - self.target_angle) // 10
        
        
        m_pressed = pygame.mouse.get_pressed()
        k_pressed = pygame.key.get_pressed()
        self.move()
        for group in self.entity_manager.entities:
            for entity in self.entity_manager.entities[group]:
                if entity.holdable:
                    self.pickup(entity, m_pressed)

        self.m_last_pressed = m_pressed
        self.k_last_pressed = k_pressed
        if self.holding != None:
            if k_pressed[pygame.K_r]:
                self.holding.rotation += 5
            self.holding.held = True
            self.holding.pos = self.pos + pygame.Vector2(0,-64).rotate(-self.angle)
       
    def pickup(self, entity, m_pressed):
        x_inrange = in_range(pygame.mouse.get_pos()[0] / SCREEN_SCALE, [entity.rect.x, entity.rect.x + entity.rect.width])
        y_inrange = in_range(pygame.mouse.get_pos()[1] / SCREEN_SCALE, [entity.rect.y, entity.rect.y + entity.rect.height])
        if entity != self.holding:
            if (entity.pos - self.pos).magnitude() <= 75:
                entity.player_inrange = True
                if x_inrange and y_inrange:
                    entity.hovered = True
                    if m_pressed[0] == True and self.m_last_pressed[0] == False and self.holding == None:
                        self.sound_manager.play_sound("pickup")
                        self.m_last_pressed = m_pressed
                        self.holding = entity
            else:
                entity.player_inrange = False
            if x_inrange and y_inrange and self.holding == None:
                entity.hovered = True
            else:
                entity.hovered = False
        else:
            entity.player_inrange = False
            entity.hovered = False
            if m_pressed[0] == True and self.m_last_pressed[0] == False and not self.holding.check_collisions() and in_range(self.holding.pos.x, [0, SCREEN_WIDTH]) and in_range(self.holding.pos.y, [0, SCREEN_HEIGHT]):
                self.game_manager.shake_screen(2,7)
                self.sound_manager.play_sound("place")
                self.holding.held = False
                self.holding = None
            if m_pressed[2] == True and self.m_last_pressed[2] == False and not self.holding.check_collisions() and in_range(self.holding.pos.x, [0, SCREEN_WIDTH]) and in_range(self.holding.pos.y, [0, SCREEN_HEIGHT]):
                self.game_manager.shake_screen(6,13)
                self.sound_manager.play_sound("throw")
                self.holding.held = False
                self.holding.velocity =( pygame.Vector2(0,-7).rotate(-self.angle))
                self.holding = None

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
        if self.pos.x + self.velocity.x > 0 and self.pos.x + self.velocity.x < SCREEN_WIDTH and self.check_collisions(self.pos + pygame.Vector2(self.velocity.x, 0)) == False:
            self.pos.x += self.velocity.x
        if self.pos.y + self.velocity.y > 0 and self.pos.y + self.velocity.y < SCREEN_HEIGHT and self.check_collisions(self.pos + pygame.Vector2(0, self.velocity.y)) == False:
            self.pos.y += self.velocity.y
        
    def draw(self, target_surface):
        temp_sprite = pygame.transform.rotate(self.sprite, self.target_angle)
        self.rect = temp_sprite.get_rect()
        temp_sprite.set_colorkey((0,0,0))
        self.rect.center = self.pos
        target_surface.blit(temp_sprite, self.rect)
    
    def get_rotation(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) / SCREEN_SCALE
        o = mouse_pos.y - self.pos.y 
        a = mouse_pos.x - self.pos.x
        if a == 0:
            a = 0.0001
        deg = math.degrees(math.atan((o)/(a))) - 90
        if mouse_pos.x < self.pos.x:
            angle = -deg
        else:
            angle = 180 - deg
        return angle
    
    def check_collisions(self, postion):
        for obsticle in self.level_manager.current_level.obsticles:
            if obsticle.collidepoint(postion):
                return True
        return False