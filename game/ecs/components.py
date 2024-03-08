import pygame
from game.ecs.entity import Entity

class Component:
    def __init__(self, parent : Entity):
        self.parent = parent

    def update(self):
        pass

    def draw(self):
        pass

class Drawable(Component):
    def __init__(self, parent : Entity, screen : pygame.Surface):
        super().__init__(parent)
        self.parent.screen = screen

class StaticSprite(Drawable):
    def __init__(self, parent : Entity, screen : pygame.Surface, image : pygame.Surface):
        super().__init__(parent, screen)
        self.parent.image = image

    def draw(self):
        self.parent.screen.blit(self.parent.image, self.parent.position)
        