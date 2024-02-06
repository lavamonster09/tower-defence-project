from misc.ui import *
from misc.theme import *
from misc.constants import *
from screens.screen import Screen
import pygame
from pygame import gfxdraw

class Game(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.back_color = DARK_BACKGROUND_COLOR
        self.game_surface = pygame.surface.Surface((SCREEN_WIDTH / 1.6, SCREEN_HEIGHT / 1.6))
        self.game_surface.set_colorkey((0,0,0))
        
    def draw(self):
        self.game_surface.fill((0,0,0))
        super().draw()
        for x in range(25):
            for y in range(14):
                pygame.draw.rect(self.game_surface, (255,255,255), (x*32,y*32,32, 32), 1)
        pygame.draw.rect(self.game_surface, (255,0,0), ((get_mouse_pos().x / 1.6) // 32 * 32 + 1, (get_mouse_pos().y / 1.6) // 32 * 32 + 1, 30, 30))
        pygame.draw.circle(self.game_surface, (255,255,255), get_mouse_pos() / 1.6, 10)
        temp_surf = pygame.transform.scale(self.game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(temp_surf,(0,0))


def get_mouse_pos() -> pygame.Vector2():
    return pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])