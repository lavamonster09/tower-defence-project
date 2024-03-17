from game.entities.entity import *

class Enemy(Entity):
    def __init__(self,game_manager, path, sprite = pygame.surface.Surface((0,0)), speed = 2) -> None:
        super().__init__(game_manager, position = path[0], sprite = sprite)
        self.speed = speed
        self.path = path
        self.current_point = 0
        self.hp = 100
        self.last_hp = self.hp

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