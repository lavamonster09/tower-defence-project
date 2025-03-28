from engine import *
from game.util.constants import *

class Upgrade(Entity):
    def __init__(self,game, position, sprite, type):
        super().__init__(game, position=position, sprite=sprite)

        self.pickup_rect = self.rect
        self.velocity = pygame.Vector2(0,0)
        self.rotation = 0

        self.hovered = False
        self.can_upgrade = False
        self.held = False
        self.last_held = False
        self.player_inrange = False
        self.holdable = True

        self.type = type

    def update(self):
        self.can_upgrade = False
        if self.check_collisions() or self.pos.x > SCREEN_WIDTH or self.pos.x < 0 or self.pos.y > SCREEN_HEIGHT or self.pos.y < 0:
            self.velocity *= -1
        for tower in self.entity_manager.entities["tower"]:
            if tower.rect.colliderect(self.pickup_rect) and self.last_held:
                if tower.can_upgrade[self.type]:
                    self.can_upgrade = True
            if tower.rect.colliderect(self.pickup_rect) and self.held == False and self.last_held == True:
                if tower.can_upgrade[self.type]:
                    self.game.popups["upgrade_decision"].set_tower(tower)
                    self.game.toggle_popup(self.game.popups["upgrade_decision"])
        self.pos += self.velocity
        self.velocity /= 1.05
        self.last_held = self.held
        super().update()

    def draw(self):
        target_surface = pygame.display.get_surface()
        target_surface.blit(self.sprite, self.rect)
        if self.hovered:
            
            self.pickup_rect.center = self.pos
            if self.player_inrange:
                for point in pygame.mask.from_surface(self.sprite.convert_alpha()).outline():
                    pygame.draw.circle(target_surface, (255,255,255), (point[0] + self.pos.x - self.rect.width/2, point[1] + self.pos.y - self.rect.height/2), 1)
            else:
                for point in pygame.mask.from_surface(self.sprite.convert_alpha()).outline():
                    pygame.draw.circle(target_surface, (255,255,255), (point[0] + self.pos.x - self.rect.width/2, point[1] + self.pos.y - self.rect.height/2), 1)
        if self.can_upgrade and self.held:
            for point in pygame.mask.from_surface(self.sprite.convert_alpha()).outline():
                pygame.draw.circle(target_surface, (255,255,255), (point[0] + self.pos.x - self.rect.width/2, point[1] + self.pos.y - self.rect.height/2), 1)
        

    def check_collisions(self):
        obsticles = [x[0] for x in self.game.level.obsticles]
        for obsticle in obsticles:
            if obsticle.collidepoint(self.pos):
                return True
        return False