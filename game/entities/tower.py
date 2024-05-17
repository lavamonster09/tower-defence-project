from msilib.schema import Upgrade
from turtle import position, speed
from game.entities.entity import *
from game.entities.bullet import *
from misc.constants import *
from misc.theme import MAIN_FONT
from misc.util import *
import pygame
import random
import math

class Tower(Entity):
    def __init__(self,game_manager, position, sprite = pygame.Surface((0,0))):
        sprite = game_manager.assets.get("tower_000")
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
        self.colided = False
        self.can_upgrade = {
                "speed" : 1,
                "damage" : 1,
                "range" : 1
            }
        

    def update(self):

        damage_upgraded = self.upgrades.count("damage") > 0 
        speed_upgraded = self.upgrades.count("speed") > 0
        range_upgraded = self.upgrades.count("range") > 0 
        if (int(damage_upgraded) + int(speed_upgraded) + int(range_upgraded)) == 2:
            self.can_upgrade = {
                    "damage": damage_upgraded,
                    "speed" : speed_upgraded,
                    "range" : range_upgraded
                }

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
                    if self.can_shoot and enemy.real_hp > 0 :
                        #self.rotation = self.get_rotation(enemy.pos)
                        self.game_manager.shake_screen(2,4)
                        self.sound_manager.play_sound("shoot")
                        enemy.real_hp -= self.damage
                        self.entity_manager.add_entity(Bullet(self.game_manager, self.game_manager.assets.get("minim"), enemy, self.pos.copy(), self.damage), "bullet")
                        self.shoot_cooldown = self.shoot_delay
                        self.can_shoot = False
        super().update()
        
    def draw(self, target_surface: pygame.Surface):
        damage = self.upgrades.count("damage")
        speed = self.upgrades.count("speed")
        range = self.upgrades.count("range")
        upgrade = f"tower_{damage}{speed}{range}"
        sprite = self.game_manager.assets.get(upgrade)
        if sprite != self.game_manager.assets.get("null"):
            self.sprite = pygame.transform.scale_by(self.game_manager.assets.get(upgrade), 2)
            self.rect = pygame.Rect(0, 0, self.sprite.get_width(), self.sprite.get_height())
            self.pickup_rect = self.rect
        font = pygame.font.Font(MAIN_FONT,20)
        temp_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        temp_sprite.set_colorkey((0,0,0))
        self.rect = temp_sprite.get_rect()
        self.rect.center = self.pos
        target_surface.blit(temp_sprite, self.rect)
        if self.hovered:
            
            self.pickup_rect.center = self.pos
            if self.can_upgrade["speed"]: target_surface.blit(font.render(str(self.upgrades.count("speed")),True,(34,177,76)), self.pickup_rect.bottomleft)
            else: target_surface.blit(font.render(str(self.upgrades.count("speed")),True,(100, 100, 100)), self.pickup_rect.bottomleft)
            if self.can_upgrade["damage"]: target_surface.blit(font.render(str(self.upgrades.count("damage")),True,(235,51,36)), pygame.Vector2(self.pickup_rect.midbottom) - pygame.Vector2(5, 0))
            else: target_surface.blit(font.render(str(self.upgrades.count("damage")),True,(100, 100, 100)), pygame.Vector2(self.pickup_rect.midbottom) - pygame.Vector2(5, 0))
            if self.can_upgrade["range"]: target_surface.blit(font.render(str(self.upgrades.count("range")),True,(230,230,230)), pygame.Vector2(self.pickup_rect.bottomright) - pygame.Vector2(10, 0))
            else: target_surface.blit(font.render(str(self.upgrades.count("range")),True,(100, 100, 100)), pygame.Vector2(self.pickup_rect.bottomright) - pygame.Vector2(10, 0))
            if self.player_inrange:
                for point in pygame.mask.from_surface(self.sprite.convert_alpha()).outline():
                    pygame.draw.rect(target_surface, (255,255,255), (point[0] + self.pos.x - self.rect.width/2, point[1] + self.pos.y - self.rect.height/2, 2, 2))
            else:
                for point in pygame.mask.from_surface(self.sprite.convert_alpha()).outline():
                    pygame.draw.rect(target_surface, (255,50, 50), (point[0] + self.pos.x - self.rect.width/2, point[1] + self.pos.y - self.rect.height/2, 2, 2))
            pygame.draw.circle(target_surface, (255,255,255), self.rect.center, self.range, 4)
        if self.held:
            for point in pygame.mask.from_surface(self.sprite.convert_alpha()).outline():
                pygame.draw.rect(target_surface, (255,255,255), (point[0] + self.pos.x - self.rect.width/2, point[1] + self.pos.y - self.rect.height/2, 2, 2))
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

        
        if upgrade.type == "range" and self.can_upgrade["range"]:
            self.range += 10 
            self.upgrades.append(upgrade.type)
        elif upgrade.type == "damage" and self.can_upgrade["damage"]:
            self.damage += 1
            self.upgrades.append(upgrade.type)
        elif upgrade.type == "speed" and self.can_upgrade["speed"]:
            self.shoot_delay -= 1
            self.upgrades.append(upgrade.type)
        else:
            upgrade.alive = True
            self.entity_manager.add_entity(upgrade, "upgrade")