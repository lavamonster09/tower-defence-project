import pygame
from game.ecs.components import *

class Entity:
    def __init__(self, components):
        self.components = {}
        self.position = pygame.Vector2(0,0)
        for component in components:
            self.add_component(component)

    def add_component(self, component: Component):
        self.components[component.__class__.__name__] = component

    def draw(self):
        for component in self.components:
            self.components[component].draw()

    def update(self):
        for component in self.components:
            self.components[component].draw()