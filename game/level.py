import pygame
import random
from misc.constants import *
from misc.util import *

class Generator():
    def __init__(self, screen_size):
        self.range_x = (0 + PATH_SIZE, screen_size[0] - PATH_SIZE)
        self.range_y = (0 + PATH_SIZE, screen_size[1] - PATH_SIZE)
        
        self.line_max_length = 100
        self.points = []
        self.obsticles = []

    def generate_level(self, no_turns, no_obsticles, line_max_length):
        self.points = self.generate_path(no_turns, line_max_length)
        self.obsticles = self.generate_obsticles(no_obsticles)
        return Level(self.points, self.obsticles)

    def generate_path(self, no_turns, line_max_length):
        direction = random.choice([pygame.Vector2(0,1), pygame.Vector2(1,0)])

        if direction.x == 0:
            points = [pygame.Vector2(self.range_x[0] - PATH_SIZE, random.uniform(self.range_y[0], self.range_y[1]))]
        else:
            points = [pygame.Vector2(random.uniform(self.range_x[0], self.range_x[1]), self.range_y[0] - PATH_SIZE)]

        current_point = points[-1]

        for _ in range(no_turns):
            current_point, direction = self.get_point(current_point, points, direction, line_max_length)
            points.append(current_point)


        final_point = direction.rotate(90)

        if final_point.x > 0 or final_point.y > 0:
            final_point.x = int(points[-1].x + final_point.x * (self.range_x[1] + PATH_SIZE - points[-1].x))
            final_point.y = int(points[-1].y + final_point.y * (self.range_y[1] + PATH_SIZE - points[-1].y))
        else:
            final_point.y = int(points[-1].x + final_point.x * points[-1].x)
            final_point.y = int(points[-1].y + final_point.y * points[-1].y
)
        points.append(final_point)

        return points

    def get_point(self, current_point, points, last_direction, line_max_length):
        direction = last_direction.rotate(random.choice([-90, 90]))

        final_point = pygame.Vector2(0,0)

        final_point.x = current_point.x + direction.x * line_max_length * random.uniform(0.1,1)
        final_point.y = current_point.y + direction.y * line_max_length * random.uniform(0.1,1)

        if not in_range(final_point.x, self.range_x) or not in_range(final_point.y, self.range_y):
            return self.get_point(current_point, points, last_direction, line_max_length)
           
        for point in points:
            if direction.x == 0:
                if in_range(final_point.y, [point.y - 20, point.y + 20]):
                    return self.get_point(current_point, points, last_direction, line_max_length)
            else:
                if in_range(final_point.x, [point.x - 20, point.x + 20]):
                    return self.get_point(current_point, points, last_direction, line_max_length)
                
        return final_point, direction

    def generate_obsticles(self, number):
        obsticles = []
        for _ in range(number):
            obsticles.append(self.get_obsticle(obsticles))
        return obsticles

    def get_obsticle(self, obsticles):
        x = int(random.uniform(self.range_x[0],self.range_x[1]))
        y = int(random.uniform(self.range_y[0], self.range_y[1]))
        obsticle = pygame.Rect(x,y ,random.randrange(MIN_OBSTICLE_SIZE, MAX_OBSTICLE_SIZE),random.randrange(MIN_OBSTICLE_SIZE, MAX_OBSTICLE_SIZE))
        collided = False
        while not self.check_obstacle(obsticle, obsticles):
            obsticle = self.get_obsticle(obsticles)
            break
        return obsticle
    
    def check_obstacle(self, obsticle, obsticles):
        rects = []
        for i in range(len(self.points) - 1):
            if self.points[i].x < self.points[i + 1].x or self.points[i].y < self.points[i + 1].y:
                width = self.points[i + 1].x - self.points[i].x
                height = self.points[i + 1].y - self.points[i].y
                rects.append(pygame.Rect(self.points[i].x  - PATH_SIZE / 2, self.points[i].y - PATH_SIZE / 2, width + PATH_SIZE, height + PATH_SIZE))
            else:
                width = self.points[i].x - self.points[i + 1].x 
                height = self.points[i].y - self.points[i + 1].y 
                rects.append(pygame.Rect(self.points[i + 1].x  - PATH_SIZE / 2, self.points[i + 1].y - PATH_SIZE / 2, width + PATH_SIZE, height + PATH_SIZE))
         
        if obsticle.collidelistall(rects) or obsticle.collidelistall(obsticles) or obsticle.right > self.range_x[1] or obsticle.bottom > self.range_y[1]:
            return False
        return True


    

class Level_manager():
    def __init__(self, scale):
        self.generator = Generator([SCREEN_WIDTH // scale, SCREEN_HEIGHT // scale])
        self.game_surf = pygame.surface.Surface((SCREEN_WIDTH // scale, SCREEN_HEIGHT // scale))
        self.current_level = Level([], [])

    def change_level(self, no_turns, no_obsticles, line_max_length):
        self.current_level = self.generator.generate_level(no_turns, no_obsticles, line_max_length)
    
    def draw(self):
        self.current_level.draw(self.game_surf)

class Level():
    def __init__(self, points, obsticles) -> None:
        self.points = points
        self.obsticles = obsticles
        self.back_color = (40,40,40)
    
    def draw(self, surface):
        surface.fill(self.back_color)
        for point in self.points:
            pygame.draw.circle(surface, (255,255,255), point, PATH_SIZE // 2)
        for i in range(len(self.points) - 1):
            pygame.draw.line(surface, (255,255,255), self.points[i], self.points[i+1], PATH_SIZE + 1)
        for obsticle in self.obsticles:
            pygame.draw.rect(surface, (200,200,200), obsticle, border_radius= PATH_SIZE // 2)
