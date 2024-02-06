import pygame
import random
from misc.util import *

class Generator():
    def __init__(self, range_x : tuple[int], range_y : tuple[int]):
        self.range_x = range_x
        self.range_y = range_y

        self.points = []
        self.obsticles = []

        self.direction = pygame.Vector2(0, 1)
        self.last_direction = pygame.Vector2(0, 1)

    def generate_random_path(self, no_turns):
        current_point = pygame.Vector2(0,random.randrange(self.range_y[0],self.range_y[1]))
        self.points.append(current_point)

        # start generation
        for i in range(no_turns):
            new_point = self.get_new_point(current_point)

            while not in_range(new_point.x, self.range_x) or not in_range(new_point.y, self.range_y):
                self.direction = self.last_direction
                new_point = self.get_new_point(current_point)

            # add point to the path
            self.points.append(new_point)
            current_point = new_point

        if self.points[-1].x != self.range_x[1] and self.direction.x == 1:
            self.points[-1].x = self.range_x[1]
        elif self.points[-1].x != self.range_x[0] and self.direction.x == -1:
            self.points[-1].x = self.range_x[0]
        elif self.points[-1].y != self.range_y[1] and self.direction.y == 1:
            self.points[-1].y = self.range_y[1]
        elif self.points[-1].y != self.range_y[0] and self.direction.y == -1:
            self.points[-1].y = self.range_y[0]

        return self.points


    def get_new_point(self, current_point):
        self.last_direction = self.direction
        self.direction = self.direction.rotate(random.choice([-90, 90]))

        new_point = pygame.Vector2()
        new_point.x = current_point.x + self.direction.x * self.range_x[0] / 2 * random.uniform(0.5, 1.5)
        new_point.y = current_point.y + self.direction.y * self.range_y[0] / 2 * random.uniform(0.5, 1.5)

        return new_point

    def generate_obsticles(self):
        pass
    
    def check_obsticle(self, obsticle):
        pass
