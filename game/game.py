
import random
from turtle import position
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
import os 

assets = {}
for file in os.scandir("assets/images"):
    if file.is_file():
        print(file.name)
    if file.is_dir():
        print("folder: "+ file.name)
        for file in os.scandir(file.path):
            print("...... "+file.name)
            if file.name.split(".")[-1] == "png":
                assets[file.name.split(".")[0]] = pygame.image.load(file.path)
                assets[file.name.split(".")[0]].set_colorkey((0,0,0))
    if file.name.split(".")[-1] == "png":
        assets[file.name.split(".")[0]] = pygame.image.load(file.path)
        assets[file.name.split(".")[0]].set_colorkey((0,0,0))

class Game(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.dev = True

        self.add_item("btn_back", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("arrow_back"), on_click= self.btn_back_on_click))
        self.add_item("dev_btn_generate", Button(BUTTON_DARK_NO_FILL , rect = (75,25,50,50), text = get_icon_hex("replay"), on_click= self.btn_generate_on_click))
        self.add_item("dev_btn_spawn_enemy", Button(BUTTON_DARK_NO_FILL , rect = (125,25,50,50), text = "E", on_click= self.btn_spawn_enemy_on_click))
        self.add_item("dev_btn_spawn_tower", Button(BUTTON_DARK_NO_FILL , rect = (175,25,50,50), text = "T", on_click= self.btn_spawn_tower_on_click))
        self.add_item("dev_btn_give_upgrade", Button(BUTTON_DARK_NO_FILL , rect = (225,25,50,50), text = "U", on_click= self.btn_give_upgrade_on_click))

        self.add_item("dev_sld_noturns", Slider(SLIDER_DARK, pos = (25, 75), length = 100, min_val = 1, max_val = 15))
        self.add_item("dev_lbl_noturns", Label(LABEL_DARK, rect = (75, 100, 125, 50), text = "No. turns: 1", font_size=20))
        self.no_turns = 1

        self.add_item("dev_sld_noboxes", Slider(SLIDER_DARK, pos = (25, 125), length = 100, min_val = 0, max_val = 5))
        self.add_item("dev_lbl_noboxes", Label(LABEL_DARK, rect = (75, 150, 125, 50), text = "No. boxes: 1", font_size=20))
        self.no_boxes = 1

        self.add_item("dev_sld_maxlinelen", Slider(SLIDER_DARK, pos = (25, 175), length = 100, min_val = 300, max_val = 1200))
        self.add_item("dev_lbl_maxlinelen", Label(LABEL_DARK, rect = (75, 200, 125, 50), text = "Max line len: 100", font_size=20))
        self.max_line_len = 300

        self.add_item("lbl_fps", Label(LABEL_DARK, rect = (98, 2, 125, 50), text = "100", font_size=20, positioning="relative"))
        
        self.game_manager = GameStateManager(self)
        
        self.game_manager.entity_manager.add_entity(Player(self.game_manager, assets["player"]), "player")
        self.toggle_dev()
    
    def draw(self):
        self.game_manager.draw(self.screen)
        super().draw()
    
    def update(self):
        self.game_manager.update()
        super().update()
        if pygame.key.get_just_pressed()[pygame.K_F5]:
            self.toggle_dev()
        self.items["lbl_fps"].text = str(int(self.screen_manager.app.clock.get_fps()))
        if int(self.items["dev_sld_noturns"].value) != self.no_turns:
            self.items["dev_lbl_noturns"].text = f"No. turns: {int(self.items['dev_sld_noturns'].value)}"
            self.no_turns = int(self.items["dev_sld_noturns"].value)
            self.game_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
        if int(self.items["dev_sld_noboxes"].value) != self.no_boxes:
            self.items["dev_lbl_noboxes"].text = f"No. boxes: {int(self.items['dev_sld_noboxes'].value)}"
            self.no_boxes = int(self.items["dev_sld_noboxes"].value)
            self.game_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
        if int(self.items["dev_sld_maxlinelen"].value) != self.max_line_len:
            self.items["dev_lbl_maxlinelen"].text = f"Max line len: {int(self.items['dev_sld_maxlinelen'].value)}"
            self.max_line_len = int(self.items["dev_sld_maxlinelen"].value)
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
        tower = Tower(self.game_manager, pygame.Vector2(SCREEN_WIDTH / 2, 0), assets["tower"])
        tower.velocity = pygame.Vector2(0,random.randrange(8,15))
        tower.velocity.rotate_ip(random.randrange(-45,45))
        self.game_manager.entity_manager.add_entity(tower, "tower")
        self.game_manager.shake_screen(10, 10)

    def btn_give_upgrade_on_click(self):
        self.game_manager.give_upgrade()

    def toggle_dev(self):
        for item in self.items:
            if item[0:3] == "dev":
                self.items[item].hidden = not self.items[item].hidden
      

class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.level_manager = level.LevelManager(SCREEN_SCALE)
        self.entity_manager = entity.EntityManager()
        self.sound_manager = sound.SoundManager()
        self.screen_offset = pygame.Vector2(0,0)
        self.shake_duration = 0 
        self.shake_strength = 0 

        self.time_paused = False
        self.current_upgrade_choices = []

    def update(self):

        self.level_manager.update()
        if not self.time_paused:
            if self.shake_duration > 0:
                dir = pygame.Vector2(0,self.shake_strength)
                dir = dir.rotate(random.randrange(360))
                self.screen_offset = dir
                self.shake_duration -= 1
            if self.shake_duration <= 0:
                self.shake_strength = 0 
                self.screen_offset = pygame.Vector2(0,0)
            self.entity_manager.update()
    
    def draw(self, screen):
        if not self.time_paused:
            self.level_manager.draw()
            self.entity_manager.draw(self.level_manager.game_surf)
        screen.fill(self.level_manager.current_level.back_color)
        screen.blit(pygame.transform.scale(self.level_manager.game_surf,( SCREEN_WIDTH, SCREEN_HEIGHT)), self.screen_offset)
    
    def change_level(self, no_turns, no_boxes, max_line_len):
        self.level_manager.change_level(no_turns, no_boxes, max_line_len)

    def spawn_enemy(self):
        enemy_sprites = []
        for i in range(1,15):
            enemy_sprites.append(assets[f"enemy{i}"])
        self.entity_manager.add_entity(Enemy(self, self.level_manager.current_level.points, random.choice(enemy_sprites), speed= 1), "enemy")
    
    def give_upgrade(self):
        self.level_manager.game_surf = pygame.transform.gaussian_blur(self.level_manager.game_surf, 2)
        self.game.add_item("btn_upgrade_1", Button(BUTTON_DARK, (20,65,300,200), "speed", positioning="relative", on_click=self.spawn_upgrade, click_args=["speed"]))
        self.game.items["btn_upgrade_1"].fore_color = (34,177,76)
        self.game.add_item("btn_upgrade_2", Button(BUTTON_DARK, (50,65,350,200), "damage", positioning="relative", on_click=self.spawn_upgrade, click_args=["damage"]))
        self.game.items["btn_upgrade_2"].fore_color = (235,51,36)
        self.game.add_item("btn_upgrade_3", Button(BUTTON_DARK, (80,65,300,200), "range", positioning="relative", on_click=self.spawn_upgrade, click_args=["range"]))
        self.game.items["btn_upgrade_3"].fore_color = (230,230,230)
        self.game.add_item("lbl_upgrade", Label(LABEL_DARK_FILLED, (50,25,650,150), f"chose an upgrade", positioning="relative", font_size=80))
        self.time_paused = True    
        
    def show_upgrade_popup(self, tower):
        self.level_manager.game_surf = pygame.transform.gaussian_blur(self.level_manager.game_surf, 2)
        self.game.add_item("btn_cancel", Button(BUTTON_DARK, (25,65,450,200), "CANCEL", positioning="relative", on_click=self.cancel_on_click))
        currently_upgrading = None 
        for upgrade in self.entity_manager.entities["upgrade"]:
            if upgrade.can_upgrade:
                currently_upgrading = upgrade
        self.game.add_item("btn_upgrade", Button(BUTTON_DARK, (75,65,450,200), "UPGRADE", positioning="relative", on_click=self.upgrade_on_click, click_args=[currently_upgrading, tower]))
        self.game.add_item("lbl_upgrade", Label(LABEL_DARK_FILLED, (50,25,650,150), f"upgrade, {currently_upgrading.type}", positioning="relative", font_size=80))
        self.time_paused = True 

    def spawn_upgrade(self, upgrade_type):
        self.shake_screen(10, 10)
        self.game.remove_item("btn_upgrade_1")
        self.game.remove_item("btn_upgrade_2")
        self.game.remove_item("btn_upgrade_3")
        self.game.remove_item("lbl_upgrade")
        upgrade = Upgrade(self, pygame.Vector2(SCREEN_WIDTH / 2, 0), assets[f"{upgrade_type}_upgrade"], upgrade_type)
        upgrade.velocity = pygame.Vector2(0,random.randrange(8,15))
        upgrade.velocity.rotate_ip(random.randrange(-45,45))
        self.entity_manager.add_entity(upgrade, "upgrade")
        self.time_paused = False

    def cancel_on_click(self):
        self.game.remove_item("btn_cancel")
        self.game.remove_item("btn_upgrade")
        self.game.remove_item("lbl_upgrade")
        self.time_paused = False

    def upgrade_on_click(self, upgrade, tower):
        self.game.remove_item("btn_cancel")
        self.game.remove_item("btn_upgrade")
        self.game.remove_item("lbl_upgrade")
        upgrade.alive = False
        tower.upgrade(upgrade)
        self.time_paused = False

    def shake_screen(self,strength, duration):
        dir = pygame.Vector2(0,strength)
        self.screen_offset += dir.rotate(random.randrange(360))
        if strength > self.shake_strength:
            self.shake_strength = strength
        self.shake_duration += duration
