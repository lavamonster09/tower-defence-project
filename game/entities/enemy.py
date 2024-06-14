from game.entities.entity import *
import random

from misc.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Enemy(Entity):
    def __init__(self,game_manager, sprite = pygame.surface.Surface((0,0)), speed = 2, children = None, path = None) -> None:
        if path is None:
            self.path = game_manager.level_manager.current_level.points
        else:
            self.path = path
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
        
class Grunt(Enemy):
    def __init__(self, game_manager, sprite=pygame.surface.Surface((0, 0)), target = pygame.Vector2(0,0)) -> None:
        speed = 1
        super().__init__(game_manager, sprite, speed, path = [pygame.Vector2(random.randrange(SCREEN_WIDTH) // 2 * 2, random.randrange(SCREEN_HEIGHT) // 2 * 2), target])
        self.hp = 30

class Boss(Entity):
    def __init__(self,game_manager, sprite = pygame.surface.Surface((0,0))) -> None:
        super().__init__(game_manager, sprite = sprite,)
        self.pos = pygame.Vector2(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        self.hp = 600
        self.no_pylons = 0

    def spawn_pylon(self):
        if self.no_pylons <= 0:
            self.entity_manager.add_entity(BossPylon(self.game_manager, self.game_manager.assets.get("pylon"), self), "pylon")
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
        super().__init__(game_manager, sprite= sprite)
        self.boss = boss
        self.pos = self.get_pos()
        self.hp = 100
        self.velocity = pygame.Vector2(0,0)
        self.last_hp = self.hp
        self.no_enemies = 5
        self.game_manager.enemies = [Grunt(self.game_manager, self.game_manager.assets.get("enemy"), self.pos) for i in range(self.no_enemies)]

    def get_pos(self):
        pos = pygame.Vector2(random.randrange(SCREEN_WIDTH) // 2 + (SCREEN_WIDTH/4), random.randrange(SCREEN_HEIGHT) // 2 + (SCREEN_HEIGHT/4))
        self.rect.center = pos
        self.boss.rect.center = self.boss.pos
        if self.rect.colliderect(self.boss.rect):
            pos = self.get_pos()
        return pos

    def update(self):
        if not self.holdable:
            self.sprite = pygame.transform.scale_by(self.game_manager.assets.get("pylon_inactive"), 2)
        else:
            self.sprite = pygame.transform.scale_by(self.game_manager.assets.get("pylon"), 2)
        self.pos += self.velocity
        if self.entity_manager.entities.get("player", [])[0].holding != self:
            if self.pos.x > SCREEN_WIDTH or self.pos.x < 0:
                self.hp = 0
            if self.pos.y > SCREEN_HEIGHT or self.pos.y < 0:
                self.hp = 0
            if self.rect.colliderect(self.boss.rect):
                self.hp = 0
                self.boss.hp -= 200
        if self.entity_manager.entities.get("enemy", []) == [] and self.game_manager.enemies == []:
            self.holdable = True
        if self.hp <= 0:
            self.sound_manager.play_sound("death")
            self.alive = False
            self.boss.no_pylons -= 1
        super().update()

    def check_collisions(self):
        for obsticle in self.level_manager.current_level.obsticles:
            if obsticle.collidepoint(self.pos):
                return True
        return False
