
import pygame
import random
from misc.constants import *
from misc.util import *

class Generator():
    def __init__(self, screen_size):
        self.range_x = (0 + PATH_SIZE, screen_size[0] - PATH_SIZE)
        self.range_y = (0 + PATH_SIZE, screen_size[1] - PATH_SIZE)
        self.direction = pygame.Vector2(0,1) 

        self.points = []
        self.obsticles = []

    def generate_level(self, no_turns, no_obsticles):
        self.points = self.generate_path(no_turns)
        return Level(self.points)

    def generate_path(self, no_turns):
        points = [pygame.Vector2(self.range_x[0] - PATH_SIZE, random.uniform(self.range_y[0], self.range_y[1]))]
        current_point = points[-1]
        for i in range(no_turns):
            current_point = self.get_point(current_point, points)
            points.append(current_point)

        final_point = self.direction.rotate(90)
        final_point.normalize_ip()

        if final_point.x > 0 or final_point.y > 0:
            final_point.x = points[-1].x + final_point.x * (self.range_x[1] + PATH_SIZE - points[-1].x)
            final_point.y = points[-1].y + final_point.y * (self.range_y[1] + PATH_SIZE - points[-1].y)
        else:
            final_point.y = points[-1].x + final_point.x * points[-1].x
            final_point.y = points[-1].y + final_point.y * points[-1].y

        points.append(final_point)

        return points

    def get_point(self, current_point, points):
        range_x = [self.range_x[0] + PATH_SIZE, self.range_x[1] - PATH_SIZE]
        range_y = [self.range_y[0] + PATH_SIZE, self.range_y[1] - PATH_SIZE]
        direction = self.direction.rotate(random.choice([-90, 90]))

        final_point = pygame.Vector2(0,0)

        final_point.x = current_point.x + direction.x * self.range_x[1] // 2 * random.uniform(0.5,1.5)
        final_point.y = current_point.y + direction.y * self.range_y[1] // 2 * random.uniform(0.5,1.5)

        if not in_range(final_point.x, self.range_x) or not in_range(final_point.y, self.range_y):
            final_point = self.get_point(current_point, points)
           
        for point in points:
        
            if direction.x == 0:
                if in_range(final_point.y, [point.y - 20, point.y + 20]):
                    final_point = self.get_point(current_point, points)
            else:
                if in_range(final_point.x, [point.x - 20, point.x + 20]):
                    final_point = self.get_point(current_point, points)

        self.direction = direction

        return final_point
    

class Level_manager():
    def __init__(self, scale):
        self.generator = Generator([SCREEN_WIDTH // scale, SCREEN_HEIGHT // scale])
        self.game_surf = pygame.surface.Surface((SCREEN_WIDTH // scale, SCREEN_HEIGHT // scale))
        self.current_level = self.generator.generate_level(6,10)

    def change_level(self, no_turns, no_obsticles):
        self.current_level = self.generator.generate_level(no_turns, no_obsticles)
    
    def draw(self):
        self.current_level.draw(self.game_surf)

class Level():
    def __init__(self, points) -> None:
        self.points = points
        self.obsticles = []
        self.back_color = (40,40,40)
    
    def draw(self, surface):
        surface.fill(self.back_color)
        for point in self.points:
            pygame.draw.circle(surface, (255,255,255), point, PATH_SIZE / 2 - 1)
        for i in range(len(self.points) - 1):
            pygame.draw.line(surface, (255,255,255), self.points[i], self.points[i+1], PATH_SIZE - 1)
