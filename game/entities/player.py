from game.entities.entity import *
import pygame
import math

class Player(Entity):
    def __init__(self, sprite = pygame.surface.Surface((0,0)), speed = 0.75) -> None:
        super().__init__(position = pygame.Vector2(0,0), sprite = sprite)
        self.speed = speed
        self.velocity = pygame.Vector2(0,0)
    
    def update(self):
        super().update()
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
        target_surface.blit(self.rotate_to_mouse_location(), self.rect)
    
    def rotate_to_mouse_location(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) / 1.6
        o = mouse_pos.y - self.pos.y 
        a = mouse_pos.x - self.pos.x
        deg = math.degrees(math.atan((o)/(a))) - 90
        if mouse_pos.x < self.pos.x:
            temp_sprite = pygame.transform.rotate(self.sprite, -deg)
        else:
            temp_sprite = pygame.transform.rotate(self.sprite, 180 - deg)
        self.rect = temp_sprite.get_rect()
        temp_sprite.set_colorkey((0,0,0))
        self.rect.center = self.pos
        return temp_sprite