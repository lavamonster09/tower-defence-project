from game.entities.entity import *

class Enemy(Entity):
    def __init__(self, path, sprite = pygame.surface.Surface((0,0)), speed = 1) -> None:
        super().__init__(position = path[0], sprite = sprite)
        self.speed = speed
        self.path = path
        self.current_point = 0

    def update(self):
        if self.current_point < len(self.path):
            if self.pos == self.path[self.current_point]:
                self.current_point += 1
            else:
                self.pos = self.pos.move_towards(self.path[self.current_point], self.speed)
        else:
            self.alive = False
        
        super().update()
    
    def draw(self, target_surface : pygame.Surface):
        return super().draw(target_surface)