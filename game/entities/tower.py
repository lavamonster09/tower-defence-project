from game.entities.entity import *
from misc.constants import *
from misc.util import *
import pygame
import math

class Tower(Entity):
    def __init__(self,game_manager, position, sprite):
        super().__init__(game_manager, position=position, sprite=sprite)
        # tower stats
        self.range = 100
        self.damage = 10
        self.shoot_delay = 10

        # tower positioning and movement
        self.pickup_rect = self.rect
        self.velocity = pygame.Vector2(0,0)
        self.rotation = 0
        
        # boolean values
        self.can_shoot = True
        self.hovered = False
        self.held = False
        self.player_inrange = False
        self.holdable = True

        # misc
        self.bullet = None
        self.shoot_cooldown = 0
        self.target = None
        self.upgrades = []

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1 
            self.can_shoot = False
        else:
            self.can_shoot = True
        if self.check_collisions() or self.pos.x > SCREEN_WIDTH or self.pos.x < 0 or self.pos.y > SCREEN_HEIGHT or self.pos.y < 0:
            self.velocity *= -1
        self.pos += self.velocity
        self.velocity /= 1.05
        if "enemy" in self.entity_manager.entities and not self.held:
            for enemy in self.entity_manager.entities["enemy"]:
                if (enemy.pos - self.pos).magnitude() < self.range:
                    if self.can_shoot:
                        self.rotation = self.get_rotation(enemy.pos)
                        self.game_manager.shake_screen(2,4)
                        self.sound_manager.play_sound("shoot")
                        enemy.hp -= self.damage
                        self.shoot_cooldown = self.shoot_delay
                        self.can_shoot = False
        super().update()
        
    def draw(self, target_surface):
        temp_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        temp_sprite.set_colorkey((0,0,0))
        self.rect = temp_sprite.get_rect()
        self.rect.center = self.pos
        target_surface.blit(temp_sprite, self.rect)
        if self.hovered:
            for upgrade in self.upgrades:
                upgrade.draw(target_surface)
            self.pickup_rect.center = self.pos
            if self.player_inrange:
                pygame.draw.rect(target_surface, (255,255,255), self.pickup_rect, 3, 2)
            else:
                pygame.draw.rect(target_surface, (255,50,50), self.pickup_rect, 3, 2)
            pygame.draw.circle(target_surface, (255,255,255), self.rect.center, self.range, 4)
        if self.held:
            pygame.draw.circle(target_surface, (255,255,255), self.rect.center, self.range, 4)

    def get_rotation(self, target):
        target
        o = target.y - self.pos.y 
        a = target.x - self.pos.x
        if a == 0:
            a = 0.0001
        deg = math.degrees(math.atan((o)/(a))) - 90
        if target.x < self.pos.x:
            angle = -deg
        else:
            angle = 180 - deg
        return angle

    def check_collisions(self):
        for obsticle in self.level_manager.current_level.obsticles:
            if obsticle.collidepoint(self.pos):
                return True
        return False

    def upgrade(self, upgrade):
        self.upgrades.append(upgrade)
        if upgrade.type == "range":
            self.range += 10 
        elif upgrade.type == "damage":
            self.damage += 1
        elif upgrade.type == "speed":
            self.shoot_delay -= 1