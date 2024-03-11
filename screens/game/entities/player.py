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
        print(self.pos, pygame.Vector2(pygame.mouse.get_pos()) / 1.6)
        target_surface.blit(self.sprite, self.rect)