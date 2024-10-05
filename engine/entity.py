import pygame

class Entity:
    def __init__(self, game, position = pygame.Vector2(0,0), sprite = pygame.Surface((0,0)), ) -> None:
        self.game = game
        self.entity_manager = game.entity_manager
        self.sound_manager = game.sound_manager
        self.level = game.level
        self.sprite = pygame.transform.scale_by(sprite,2)
        self.rect = pygame.Rect(0, 0, self.sprite.get_width(), self.sprite.get_height())
        self.rect.center = position
        self.pos = position
        self.velocity = None
        self.alive = True
        self.holdable = False
        self.zindex = 0
    
    def draw(self):
        surface = pygame.display.get_surface()
        surface.blit(self.sprite, self.rect)
    
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
        for group in self.entities.copy():
            for entity in self.entities[group]:
                entity.update()
                if not entity.alive:
                    self.remove_entity(entity, group)
                if entity.holdable:
                    if entity.rect.collidepoint(pygame.Vector2(pygame.mouse.get_pos())):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def draw(self):
        draw_order = []
        for group in self.entities:
            for entity in self.entities[group]:
                draw_order.append((entity.zindex ,entity))
        draw_order.sort()
        for entity in draw_order:
            entity[1].draw()