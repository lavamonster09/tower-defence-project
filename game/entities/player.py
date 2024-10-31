from engine import *
from game.util.constants import *
import pygame


class Player(Entity):
    def __init__(self, game, image, speed = 1.4) -> None:
        super().__init__(game, position = pygame.Vector2(0,0), sprite = game.assets.get(image))
        # player stats
        self.speed = speed

        # player positioning and movement
        self.velocity = pygame.Vector2(0,0)
        self.m_last_pressed = pygame.mouse.get_pressed()
        self.k_last_pressed = pygame.key.get_pressed()
        self.target_angle = 0
        self.angle = 0

        # boolean values
        self.holding = None
        self.input_lock = False
        self.prev_input_lock = True

        # misc
        self.keybinds = game.keybinds
        self.zindex = 2
        self.pos = pygame.Vector2(int(self.game.config.get("SCREEN_WIDTH")) // 2, -60)
        self.last_pos = pygame.Vector2(int(self.game.config.get("SCREEN_WIDTH")) // 2, int(self.game.config.get("SCREEN_HEIGHT")) // 2)
    
    def update(self):
        super().update()
        if self.input_lock:
            if self.prev_input_lock != self.input_lock:
                print(self.prev_input_lock, self.input_lock)
                self.last_pos = self.pos.copy()
                self.prev_input_lock = self.input_lock
            if self.pos.y > -60:
                self.pos.y -= 10
                self.target_angle += 10
                if self.target_angle > 360 or self.target_angle < 0:
                    self.target_angle %= 360
            return

        if not self.input_lock:
            if self.pos.y < self.last_pos.y:
                self.pos.y += 10
                self.target_angle += 10
                if self.target_angle > 360 or self.target_angle < 0:
                    self.target_angle %= 360
                return
            else:
                if self.check_collisions(self.pos):
                    self.last_pos.y += 10
                    return
                self.last_pos = self.pos

        self.prev_input_lock = self.input_lock
        self.target_angle = self.get_rotation()
        
        if self.angle > 360 or self.angle < 0:
            self.angle %= 360

        if (self.target_angle + 360 - self.angle) / 10 < (self.angle - self.target_angle) / 10:
            self.angle += abs((self.target_angle + 360 - self.angle) // 10)
        elif (self.target_angle - self.angle) / 10 > (self.angle + 360 - self.target_angle) / 10:
            self.angle -= abs((self.angle + 360 - self.target_angle) // 10)
        else:
            self.angle -= (self.angle - self.target_angle) // 10
        
        
        m_pressed = pygame.mouse.get_pressed()
        k_pressed = pygame.key.get_pressed()
        self.move()
        for group in self.entity_manager.entities:
            for entity in self.entity_manager.entities[group]:
                if entity.holdable:
                    self.pickup(entity, m_pressed)

        self.m_last_pressed = m_pressed
        self.k_last_pressed = k_pressed
        if self.holding != None:
            self.holding.held = True
            self.holding.pos = self.pos + pygame.Vector2(0,-64).rotate(-self.angle)
       
    def pickup(self, entity, m_pressed):
        x_inrange = in_range(pygame.mouse.get_pos()[0] / SCREEN_SCALE, [entity.rect.x, entity.rect.x + entity.rect.width])
        y_inrange = in_range(pygame.mouse.get_pos()[1] / SCREEN_SCALE, [entity.rect.y, entity.rect.y + entity.rect.height])
        if entity != self.holding:
            if (entity.pos - self.pos).magnitude() <= 75:
                entity.player_inrange = True
                if x_inrange and y_inrange:
                    entity.hovered = True
                    if m_pressed[0] == True and self.m_last_pressed[0] == False and self.holding == None:
                        self.sound_manager.play_sound("pickup")
                        self.m_last_pressed = m_pressed
                        self.holding = entity
            else:
                entity.player_inrange = False
            if x_inrange and y_inrange and self.holding == None:
                entity.hovered = True
            else:
                entity.hovered = False
        else:
            entity.player_inrange = False
            entity.hovered = False
            if m_pressed[0] == True and self.m_last_pressed[0] == False and not self.holding.check_collisions() and in_range(self.holding.pos.x, [0, SCREEN_WIDTH]) and in_range(self.holding.pos.y, [0, SCREEN_HEIGHT]):
                self.sound_manager.play_sound("place")
                self.holding.held = False
                self.holding = None
            if m_pressed[2] == True and self.m_last_pressed[2] == False and not self.holding.check_collisions() and in_range(self.holding.pos.x, [0, SCREEN_WIDTH]) and in_range(self.holding.pos.y, [0, SCREEN_HEIGHT]):
                self.sound_manager.play_sound("throw")
                self.holding.held = False
                self.holding.velocity =( pygame.Vector2(0,-7).rotate(-self.angle))
                self.holding = None

    def move(self):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0,0)
        if keys[self.keybinds.get("up", -1)]:
            direction.y -= 1
        if keys[self.keybinds.get("left", -1)]:
            direction.x -= 1
        if keys[self.keybinds.get("down", -1)]:
            direction.y += 1
        if keys[self.keybinds.get("right", -1)]:
            direction.x += 1 
        
        if not direction == pygame.Vector2(0,0):
            direction = direction.normalize()    
        
        self.velocity /= 1.2
         
        
        self.velocity += self.speed * direction
        if self.pos.x + self.velocity.x > 0 and self.pos.x + self.velocity.x < SCREEN_WIDTH and self.check_collisions(self.pos + pygame.Vector2(self.velocity.x, 0)) == False:
            self.pos.x += self.velocity.x
        if self.pos.y + self.velocity.y > 0 and self.pos.y + self.velocity.y < SCREEN_HEIGHT and self.check_collisions(self.pos + pygame.Vector2(0, self.velocity.y)) == False:
            self.pos.y += self.velocity.y
        
    def draw(self):
        surface = pygame.display.get_surface()
        temp_sprite = pygame.transform.scale_by(self.sprite, 0.5)
        temp_sprite = self.game.assets.get_frame("tvman", int(self.target_angle//45))
        temp_sprite = pygame.transform.scale_by(temp_sprite, 2)
        self.rect = temp_sprite.get_rect()
        temp_sprite.set_colorkey((0,0,0))
        self.rect.center = self.pos
        surface.blit(temp_sprite, self.rect)
    
    def get_rotation(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) / SCREEN_SCALE
        o = mouse_pos.y - self.pos.y 
        a = mouse_pos.x - self.pos.x
        if a == 0:
            a = 0.0001
        deg = math.degrees(math.atan((o)/(a))) - 90
        if mouse_pos.x < self.pos.x:
            angle = -deg
        else:
            angle = 180 - deg
        return angle
    
    def check_collisions(self, pos):
        rect = pygame.Rect(0, 0, self.sprite.get_width(), self.sprite.get_height())
        rect.center = pos
        obsticles = [x[0] for x in self.game.level.obsticles]
        for obsticle in obsticles:
            if obsticle.colliderect(rect):
                return True
        return False