
import random
from misc.ui import *
from misc.theme import *
from misc.constants import *
from screens.screen import Screen
from game.entities.enemy import Enemy
from game.entities.player import Player
from game.entities.tower import Tower
from game.entities.upgrade import Upgrade
import game.sound as sound
import game.entities.entity as entity
import game.level as level
import pygame

class Game(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)

        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("arrow_back"), on_click= self.btn_back_on_click))
        self.add_item("btn_generate", Button(BUTTON_DARK_NO_FILL , rect = (75,25,50,50), text = get_icon_hex("replay"), on_click= self.btn_generate_on_click))
        self.add_item("btn_spawn_enemy", Button(BUTTON_DARK_NO_FILL , rect = (125,25,50,50), text = "E", on_click= self.btn_spawn_enemy_on_click))
        self.add_item("btn_spawn_tower", Button(BUTTON_DARK_NO_FILL , rect = (175,25,50,50), text = "T", on_click= self.btn_spawn_tower_on_click))
        self.add_item("btn_give_upgrade", Button(BUTTON_DARK_NO_FILL , rect = (225,25,50,50), text = "U", on_click= self.btn_give_upgrade_on_click))

        self.add_item("sld_noturns", Slider(SLIDER_DARK, pos = (25, 75), length = 100, min_val = 1, max_val = 15))
        self.add_item("lbl_noturns", Label(LABEL_DARK, rect = (75, 100, 125, 50), text = "No. turns: 1", font_size=20))
        self.no_turns = 1

        self.add_item("sld_noboxes", Slider(SLIDER_DARK, pos = (25, 125), length = 100, min_val = 0, max_val = 5))
        self.add_item("lbl_noboxes", Label(LABEL_DARK, rect = (75, 150, 125, 50), text = "No. boxes: 1", font_size=20))
        self.no_boxes = 1

        self.add_item("sld_maxlinelen", Slider(SLIDER_DARK, pos = (25, 175), length = 100, min_val = 300, max_val = 1200))
        self.add_item("lbl_maxlinelen", Label(LABEL_DARK, rect = (75, 200, 125, 50), text = "Max line len: 100", font_size=20))
        self.max_line_len = 300
        
        self.game_manager = GameStateManager(self)
        
        self.game_manager.entity_manager.add_entity(Player(self.game_manager, pygame.image.load(r"assets\images\player.png").convert()), "player")
    
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
        self.game_manager.sound_manager.play_sound("click")
        self.screen_manager.change_screen(self.screen_manager.before_last_screen, 20)
        
    def btn_generate_on_click(self):
        self.game_manager.sound_manager.play_sound("click")
        self.game_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
        self.game_manager.entity_manager.remove_group("enemy")
    
    def btn_spawn_enemy_on_click(self):
        self.game_manager.sound_manager.play_sound("click")
        self.game_manager.spawn_enemy()
        
    def btn_spawn_tower_on_click(self):
        self.game_manager.sound_manager.play_sound("click")
        img = pygame.image.load(r"assets\images\tower.png").convert()
        img.set_colorkey((0,0,0))
        self.game_manager.entity_manager.add_entity(Tower(self.game_manager, pygame.Vector2(100,100), img), "tower")

    def btn_give_upgrade_on_click(self):
        self.game_manager.give_upgrade()

class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.level_manager = level.LevelManager(SCREEN_SCALE)
        self.entity_manager = entity.EntityManager()
        self.sound_manager = sound.SoundManager()

        self.time_paused = False
        self.current_upgrade_choices = []

    def update(self):
        self.level_manager.update()
        if not self.time_paused:
            self.entity_manager.update()
    
    def draw(self, screen):
        if not self.time_paused:
            self.level_manager.draw()
            self.entity_manager.draw(self.level_manager.game_surf)
        screen.blit(pygame.transform.scale(self.level_manager.game_surf,( SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
    
    def change_level(self, no_turns, no_boxes, max_line_len):
        self.level_manager.change_level(no_turns, no_boxes, max_line_len)

    def spawn_enemy(self):
        img = pygame.image.load(r"assets\images\enemy.png").convert()
        img.set_colorkey((0,0,0))
        self.entity_manager.add_entity(Enemy(self, self.level_manager.current_level.points, img, speed= 1), "enemy")
    
    def give_upgrade(self):
        self.level_manager.game_surf = pygame.transform.gaussian_blur(self.level_manager.game_surf, 2)
        self.game.add_item("btn_upgrade_1", Button(BUTTON_DARK, (20,50,200,200), "1", positioning="relative", on_click=self.spawn_upgrade, click_args=["upgrade_1"]))
        self.game.add_item("btn_upgrade_2", Button(BUTTON_DARK, (50,50,200,200), "2", positioning="relative", on_click=self.spawn_upgrade, click_args=["upgrade_2"]))
        self.game.add_item("btn_upgrade_3", Button(BUTTON_DARK, (80,50,200,200), "3", positioning="relative", on_click=self.spawn_upgrade, click_args=["upgrade_3"]))
        self.time_paused = True    
        
    def show_upgrade_popup(self):
        self.level_manager.game_surf = pygame.transform.gaussian_blur(self.level_manager.game_surf, 2)
        self.game.add_item("btn_cancel", Button(BUTTON_DARK, (20,50,200,200), "CANCEL", positioning="relative", on_click=self.cancel_on_click))
        self.game.add_item("btn_upgrade", Button(BUTTON_DARK, (80,50,200,200), "UPGRADE", positioning="relative", on_click=self.spawn_upgrade, click_args=["upgrade_2"]))
        self.time_paused = True 

    def spawn_upgrade(self, upgrade):
        self.game.remove_item("btn_upgrade_1")
        self.game.remove_item("btn_upgrade_2")
        self.game.remove_item("btn_upgrade_3")
        print(upgrade)
        upgrade = Upgrade(self, pygame.Vector2(SCREEN_WIDTH / 2, 0), pygame.image.load(r"assets\images\enemy.png").convert())
        upgrade.velocity = pygame.Vector2(0,random.randrange(8,15))
        upgrade.velocity.rotate_ip(random.randrange(-45,45))
        self.entity_manager.add_entity(upgrade, "upgrade")
        self.time_paused = False

    def cancel_on_click(self):
        self.game.remove_item("btn_cancel")
        self.game.remove_item("btn_upgrade")
        self.time_paused = False