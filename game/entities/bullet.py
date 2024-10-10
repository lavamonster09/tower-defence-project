from engine import *

class Bullet(Entity):
    def __init__(self,game_manager, sprite = pygame.surface.Surface((0,0)), target = None, start_pos = pygame.Vector2(0,0), damage = 0) -> None:
        super().__init__(game_manager, position = start_pos, sprite = sprite)
        self.target = target
        self.damage = damage
        self.speed = 3

    def update(self):
        if self.pos != self.target.pos:
            self.speed += 0.2
            self.pos.move_towards_ip(self.target.pos, self.speed)
        if self.pos.distance_to(self.target.pos) <= 1:
            self.target.hp -= self.damage
            self.alive = False
        super().update()
    