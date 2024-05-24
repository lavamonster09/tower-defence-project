from game.entities.entity import *
import random

from misc.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Enemy(Entity):
    def __init__(self,game_manager, sprite = pygame.surface.Surface((0,0)), speed = 2, children = None) -> None:
        self.path = game_manager.level_manager.current_level.points
        super().__init__(game_manager, position = self.path[0], sprite = sprite)
        self.speed = speed
        self.current_point = 0
        self.hp = 100
        self.real_hp = 100 
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
        
class Boss(Entity):
    def __init__(self,game_manager, sprite = pygame.surface.Surface((0,0))) -> None:
        super().__init__(game_manager, sprite = pygame.transform.scale_by(sprite, 2))
        self.pos = pygame.Vector2(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        self.hp = 500
        self.no_pylons = 0

    def spawn_pylon(self):
        if self.no_pylons <= 0:
            self.entity_manager.add_entity(BossPylon(self.game_manager, self.game_manager.assets.get("pylon"), self), "enemy")
            self.no_pylons += 1 

    def update(self):
        
        if self.hp <= 0:
            self.sound_manager.play_sound("death")
            self.alive = False
        if self.alive:
            self.spawn_pylon()

        return super().update()
    
    def draw(self, target_surface : pygame.Surface):
        rect = pygame.Rect(0,0,self.hp, 20)
        rect.midtop = (SCREEN_WIDTH/2, 10)
        pygame.draw.rect(target_surface, (255,55,55), rect)
        return super().draw(target_surface)

class BossPylon(Entity):
    def __init__(self,game_manager, sprite = pygame.surface.Surface((0,0)), boss = None) -> None:
        super().__init__(game_manager, sprite = pygame.transform.scale_by(sprite, 2))
        self.pos = pygame.Vector2(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT))
        self.hp = 100
        self.real_hp = 100
        self.boss = boss
        self.last_hp = self.hp
        self.protected = True 
        self.no_enemies = 10

    def update(self):
        if self.protected: 
            self.real_hp = 0
        if self.hp <= 0:
            self.sound_manager.play_sound("death")
            self.alive = False
            self.boss.no_pylons -= 1
        super().update()
        if not self.protected:
            self.boss.hp -= (self.last_hp - self.hp)
        elif self.last_hp != self.hp:
             self.hp += (self.last_hp - self.hp)   
        self.last_hp = self.hp