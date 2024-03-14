from misc.ui import *
from misc.theme import *
from misc.constants import *
from screens.screen import Screen
from game.entities.enemy import Enemy
from game.entities.player import Player
from game.entities.tower import Tower
import game.entities.entity as entity
import game.level as level
import pygame

class Game(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)

        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("arrow_back"), on_click= self.btn_back_on_click))
        self.add_item("btn_generate", Button(BUTTON_DARK_NO_FILL , rect = (75,25,50,50), text = get_icon_hex("replay"), on_click= self.btn_generate_on_click))
        self.add_item("btn_spawn_enemy", Button(BUTTON_DARK_NO_FILL , rect = (125,25,50,50), text = "+", on_click= self.btn_spawn_enemy_on_click))

        self.add_item("sld_noturns", Slider(SLIDER_DARK, pos = (25, 75), length = 100, min_val = 1, max_val = 15))
        self.add_item("lbl_noturns", Label(LABEL_DARK, rect = (75, 100, 125, 50), text = "No. turns: 1", font_size=20))
        self.no_turns = 1

        self.add_item("sld_noboxes", Slider(SLIDER_DARK, pos = (25, 125), length = 100, min_val = 0, max_val = 5))
        self.add_item("lbl_noboxes", Label(LABEL_DARK, rect = (75, 150, 125, 50), text = "No. boxes: 1", font_size=20))
        self.no_boxes = 1

        self.add_item("sld_maxlinelen", Slider(SLIDER_DARK, pos = (25, 175), length = 100, min_val = 300, max_val = 1200))
        self.add_item("lbl_maxlinelen", Label(LABEL_DARK, rect = (75, 200, 125, 50), text = "Max line len: 100", font_size=20))
        self.max_line_len = 300
        
        self.game_manager = GameStateManager()
        
        self.game_manager.entity_manager.add_entity(Player(self.game_manager.entity_manager, pygame.image.load(r"assets\images\player.png").convert()), "player")
    
    def draw(self):
        self.game_manager.draw(self.screen)
        super().draw()
    
    def update(self):
        self.game_manager.update()
        super().update()
        if int(self.items["sld_noturns"].value) != self.no_turns:
            self.items["lbl_noturns"].text = f"No. turns: {int(self.items['sld_noturns'].value)}"
            self.no_turns = int(self.items["sld_noturns"].value)
            self.game_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
        if int(self.items["sld_noboxes"].value) != self.no_boxes:
            self.items["lbl_noboxes"].text = f"No. boxes: {int(self.items['sld_noboxes'].value)}"
            self.no_boxes = int(self.items["sld_noboxes"].value)
            self.game_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
        if int(self.items["sld_maxlinelen"].value) != self.max_line_len:
            self.items["lbl_maxlinelen"].text = f"Max line len: {int(self.items['sld_maxlinelen'].value)}"
            self.max_line_len = int(self.items["sld_maxlinelen"].value)
            self.game_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
    
    def btn_back_on_click(self):
        self.screen_manager.change_screen(self.screen_manager.before_last_screen, 20)
        
    def btn_generate_on_click(self):
        self.game_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
        self.game_manager.entity_manager.remove_group("enemy")
    
    def btn_spawn_enemy_on_click(self):
        self.game_manager.spawn_enemy()
        img = pygame.image.load(r"assets\images\tower.png").convert()
        img.set_colorkey((0,0,0))
        self.game_manager.entity_manager.add_entity(Tower(pygame.Vector2(100,100), img), "tower")

class GameStateManager:
    def __init__(self):
        self.level_manager = level.LevelManager(SCREEN_SCALE)
        self.entity_manager = entity.EntityManager()
    
    def update(self):
        self.level_manager.update()
        self.entity_manager.update()
    
    def draw(self, screen):
        self.level_manager.draw()
        self.entity_manager.draw(self.level_manager.game_surf)
        screen.blit(pygame.transform.scale(self.level_manager.game_surf,( SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
    
    def change_level(self, no_turns, no_boxes, max_line_len):
        self.level_manager.change_level(no_turns, no_boxes, max_line_len)

    def spawn_enemy(self):
        img = pygame.image.load(r"assets\images\enemy.png").convert()
        img.set_colorkey((0,0,0))
        self.entity_manager.add_entity(Enemy(self.level_manager.current_level.points, img, speed= 1), "enemy")
    