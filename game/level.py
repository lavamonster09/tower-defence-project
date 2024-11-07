import pygame
import random
from .util import *


class Generator:
    def __init__(self, screen_size, game):
        self.level_number = 1
        self.game = game
        self.range_x = (0 + PATH_SIZE, screen_size[0] - PATH_SIZE)
        self.range_y = (0 + PATH_SIZE, screen_size[1] - PATH_SIZE)
        
        self.line_max_length = 100
        self.points = []
        self.obsticles = []
        self.obsticle_sprites = []
        self.decoration_sprites = []

    def generate_level(self, level_data):
        self.obsticle_sprites = []
        self.decoration_sprites = []
        for asset in self.game.assets.assets:
            split = asset.split("_")
            if asset.startswith("ob"):
                if split[1] == str(level_data["level_no"]):
                    self.obsticle_sprites.append(pygame.transform.scale_by(self.game.assets.get(asset),2))
            if asset.startswith("de"):
                if split[1] == str(level_data["level_no"]):
                    self.decoration_sprites.append(pygame.transform.scale_by(self.game.assets.get(asset),2))
        self.points = self.generate_path(level_data["no_turns"], level_data["max_line_len"])
        self.obsticles = self.generate_obsticles(level_data["no_boxes"])
        return Level(self.game, self.points, self.obsticles, level_data["level_no"])

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

        if final_point.x == 0:
            if final_point.y > 0:
                final_point.x = points[-1].x
                final_point.y = self.range_y[1] + PATH_SIZE
            if final_point.y < 0:
                final_point.x = points[-1].x
                final_point.y = self.range_y[0] - PATH_SIZE
        else:
            if final_point.x > 0:
                final_point.x = self.range_x[1] + PATH_SIZE
                final_point.y = points[-1].y
            if final_point.x < 0:
                final_point.x = self.range_x[0] - PATH_SIZE
                final_point.y = points[-1].y

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

    def generate_decorations(self, number, obsticles):
        decorations = []
        for _ in range(number):
            decorations.append(self.get_decoration(obsticles))
        return decorations

    def get_obsticle(self, obsticles):
        x = int(random.uniform(self.range_x[0],self.range_x[1]))
        y = int(random.uniform(self.range_y[0], self.range_y[1]))   
        sprite = random.choice(self.obsticle_sprites)
        obsticle = sprite.get_rect()
        obsticle.center = (x,y)
        _r = obsticle, sprite
        while not self.check_obstacle(obsticle, obsticles):
            _r = self.get_obsticle(obsticles)
            break
        return _r
    
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
         
        if obsticle.collidelistall(rects) or obsticle.collidelistall([x[0] for x in obsticles]) or obsticle.right > self.range_x[1] or obsticle.bottom > self.range_y[1]:
            return False
        return True

class Level():
    def __init__(self, game, points, obsticles, level_number) -> None:
        self.game = game
        self.level_number = level_number
        self.background = pygame.image.load(f"assets\images/area_{level_number}/floor.png").convert()
        self.background = pygame.transform.scale_by(self.background,2)
        self.points = points
        self.obsticles = obsticles
        self.back_color = (30, 74, 157)
    
    def draw(self):
        surface = pygame.display.get_surface()
        surface.blit(self.background, (0,0))
        

        for i in range(len(self.points) - 1):
            point1 = (self.points[i][0] // 2 * 2, self.points[i][1] // 2 * 2)
            point2 = (self.points[i+1][0] // 2 * 2, self.points[i+1][1] // 2 * 2)
            pygame.draw.line(surface, (46, 34, 47), point1, point2, PATH_SIZE + 5)
            
        for point in self.points:
            point = (point[0] // 2 * 2, point[1] // 2 * 2)
            rect = pygame.Rect(0,0,PATH_SIZE + 1, PATH_SIZE + 1)
            rect2 = pygame.Rect(0,0, PATH_SIZE + 5, PATH_SIZE + 5)
            rect.center = point
            rect2.center = point
            pygame.draw.rect(surface, (46, 34, 47), rect2)
            pygame.draw.rect(surface, (62, 53, 70), rect)
        for i in range(len(self.points) - 1):
            point = pygame.Vector2(self.points[i][0] // 2 * 2, self.points[i][1] // 2 * 2)
            point2 = pygame.Vector2(self.points[i+1][0] // 2 * 2, self.points[i+1][1] // 2 * 2)
            length = point.distance_to(point2)
            slope = point2 - point
            slope = slope.normalize()
            for index in range(0, int(length/6), 2):
                start = point + (slope *    index    *6)
                end   = point + (slope * (index + 1) *6)
                pygame.draw.line(surface, (255,255,255), start, end, 3)
        
        pygame.draw.circle(surface, (30, 188, 115), self.points[0], PATH_SIZE/2 + 3)
        pygame.draw.circle(surface, (35, 144, 99), self.points[0], PATH_SIZE/2 + 3, 3)
            
        for obsticle in self.obsticles:
            sprite = obsticle[1]
            rect = sprite.get_rect()
            surface.blit(sprite, obsticle[0])
        
    def update(self):
        pass

class BossLevel:
    def __init__(self,game, level_no) -> None:
        self.game = game
        self.background = pygame.image.load(f"assets\images/area_{level_no}/floor.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.points = []
        self.obsticles = []
        self.level_number = level_no

    def draw(self):
        self.game.screen.blit(self.background, (0,0))