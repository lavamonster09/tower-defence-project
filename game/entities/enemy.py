from engine import *

from game.util.constants import *

class Enemy(Entity):
    def __init__(self,game, sprite = pygame.surface.Surface((0,0)), speed = 2, children = None, path = None) -> None:
        if path is None:
            self.path = game.level.points
        else:
            self.path = path
        super().__init__(game, position = self.path[0], sprite = sprite)
        self.speed = speed
        self.current_point = 0
        self.hp = self.hp
        self.real_hp = self.hp
        self.last_hp = self.hp
        self.children = children
        self.zindex = 0

    def update(self):
        if self.current_point < len(self.path):
            if self.pos == self.path[self.current_point]:
                self.current_point += 1
            else:
                self.pos = self.pos.move_towards(self.path[self.current_point], self.speed)
        else:
            self.alive = False
            self.game.hp -= self.hp
            if self.game.hp <= 0:
                self.game.toggle_popup(self.game.popups["death"])
        if self.hp <= 0:
            self.sound_manager.play_sound("death")
            self.alive = False
        super().update()
    
    def draw(self):
        super().draw()
        if self.last_hp != self.hp:
            self.last_hp = self.hp

class Standard(Enemy):
    def __init__(self, game_manager, sprite=pygame.surface.Surface((0, 0))) -> None:
        speed = 2
        self.hp = 100
        super().__init__(game_manager, sprite, speed)
        
class Fast(Enemy):
    def __init__(self, game_manager, sprite=pygame.surface.Surface((0, 0))) -> None:
        speed = 3
        self.hp = 100
        super().__init__(game_manager, sprite, speed)

class Boss(Enemy):
    def __init__(self, game_manager, sprite=pygame.surface.Surface((0, 0))) -> None:
        speed = 0.5
        self.hp = 100 * game_manager.current_round.round_number
        super().__init__(game_manager, sprite, speed)

    def update(self):
        if self.hp <= 0:
            self.game.level_data["level_no"] += 1 
            self.game.draw_queue.remove((1, self.game.level))
            self.game.level = self.game.generator.generate_level(self.game.level_data)
            self.game.draw_queue.append((1, self.game.level))
        return super().update()

    def draw(self):
        rect = pygame.Rect(0,0,self.hp, 20)
        rect.midtop = (SCREEN_WIDTH/2, 10)
        pygame.draw.rect(self.game.screen, (255,55,55), rect)
        return super().draw()