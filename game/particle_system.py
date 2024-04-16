import pygame

class ParticleSystem:
    def __init__(self):
        self.particles = []

class Particle:
    def __init__(self) -> None:
        self.alive = True
        self.pos = pygame.Vector2(0,0)
        self.veclocity = pygame.Vector2(0,0)
        self.age = 0
        self.lifespan = 0
        self.start_size = 0
        self.end_size = 0
        self.start_opasity = 0
        self.end_opsasity = 0 
        self.shaper = "circle"
        self.surface = None

    def draw(self, target):
        pass

    def update(self):
        pass
