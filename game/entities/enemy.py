from game.entities.entity import *
import random

class Enemy(Entity):
    def __init__(self,game_manager, sprite = pygame.surface.Surface((0,0)), speed = 2, children = None) -> None:
        self.path = game_manager.level_manager.current_level.points
        super().__init__(game_manager, position = self.path[0], sprite = sprite)
        self.speed = speed
        self.current_point = 0
        self.hp = 100
        self.last_hp = self.hp
        self.children = children

    def update(self):
        if self.current_point < len(self.path):
            if self.pos == self.path[self.current_point]:
                self.current_point += 1
            else:
                self.pos = self.pos.move_towards(self.path[self.current_point], self.speed)
        else:
            self.alive = False
        if self.hp <= 0:
            self.sound_manager.play_sound("death")
            self.alive = False
        super().update()
    
    def draw(self, target_surface : pygame.Surface):
        super().draw(target_surface)
        if self.last_hp != self.hp:
            self.last_hp = self.hp

class Standard(Enemy):
    def __init__(self, game_manager, sprite=pygame.surface.Surface((0, 0))) -> None:
        speed = 2
        super().__init__(game_manager, sprite, speed)
        
class Fast(Enemy):
    def __init__(self, game_manager, sprite=pygame.surface.Surface((0, 0))) -> None:
        speed = 3
        super().__init__(game_manager, sprite, speed)
        