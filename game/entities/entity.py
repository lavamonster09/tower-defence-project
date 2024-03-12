import pygame

class Entity:
    def __init__(self, position = pygame.Vector2(0,0), sprite = pygame.Surface((0,0))) -> None:
        self.rect = pygame.Rect(0, 0, sprite.get_width(), sprite.get_height())
        self.rect.center = position
        self.pos = position
        self.sprite = sprite
        self.alive = True
    
    def draw(self, target_surface):
        target_surface.blit(self.sprite, self.rect)
    
    def update(self):
        self.rect.center = self.pos

class EntityManager:
    def __init__(self) -> None:
        self.entities = {}

    def add_entity(self, entity, group):
        if group in self.entities:
            self.entities[group].append(entity)
        else:
            self.entities[group] = [entity]
    
    def remove_entity(self, entity, group):
        if group in self.entities:
            self.entities[group].remove(entity)
    
    def remove_group(self, group):
        if group in self.entities:
            del self.entities[group]

    def update(self):
        for group in self.entities:
            for entity in self.entities[group]:
                entity.update()
                if not entity.alive:
                    self.remove_entity(entity, group)

    def draw(self, target_surface):
        for group in self.entities:
            for entity in self.entities[group]:
                entity.draw(target_surface)
    