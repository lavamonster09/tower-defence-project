
import random
from turtle import position
from misc.ui import *
from misc.theme import *
from misc.constants import *
from screens.screen import Screen
from game.entities.enemy import *
from game.entities.player import Player
from game.entities.tower import Tower
from game.entities.upgrade import Upgrade
import game.sound as sound
import game.entities.entity as entity
import game.level as level
import pygame
import time 
import os 

class Assets: 
    def __init__(self) -> None:
        self.assets = {}
        self.load()
    
    def load(self):
        for file in os.scandir("assets/images"):
            if file.is_file():
                print(file.name)
            if file.is_dir():
                print("folder: "+ file.name)
                for file in os.scandir(file.path):
                    print("...... "+file.name)
                    if file.name.split(".")[-1] == "png":
                        self.assets[file.name.split(".")[0]] = pygame.image.load(file.path)
                        self.assets[file.name.split(".")[0]].set_colorkey((0,0,0))
            if file.name.split(".")[-1] == "png":
                self.assets[file.name.split(".")[0]] = pygame.image.load(file.path)
                self.assets[file.name.split(".")[0]].set_colorkey((0,0,0))
    def get(self, key):
        return self.assets.get(key, self.assets["null"])


class Game(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.dev = True
        self.assets = Assets()
        
        self.game_manager = GameStateManager(self)
        self.add_item("dev_btn_reload", Button(BUTTON_DARK_NO_FILL , rect = (75,25,50,50), text = get_icon_hex("replay"), on_click= self.btn_reload_on_click))
        self.add_item("dev_btn_generate", Button(BUTTON_DARK_NO_FILL , rect = (25,25,50,50), text = get_icon_hex("replay"), on_click= self.btn_generate_on_click))
        self.add_item("dev_btn_spawn_enemy", Button(BUTTON_DARK_NO_FILL , rect = (125,25,50,50), text = "E", on_click= self.btn_spawn_enemy_on_click))
        self.add_item("dev_btn_spawn_tower", Button(BUTTON_DARK_NO_FILL , rect = (175,25,50,50), text = "T", on_click= self.btn_spawn_tower_on_click))
        self.add_item("dev_btn_give_upgrade", Button(BUTTON_DARK_NO_FILL , rect = (225,25,50,50), text = "U", on_click= self.btn_give_upgrade_on_click))

        self.no_turns = 6
        self.no_boxes = 6
        self.max_line_len = 1000

        self.add_item("lbl_fps", Label(LABEL_DARK, rect = (98, 98, 125, 50), text = "100", font_size=20, positioning="relative"))
        self.add_item("lbl_round", Label(LABEL_DARK, rect = (98, 2, 125, 50), text = "0", font_size=30, positioning="relative"))
        self.add_item("btn_roundstart", Button(BUTTON_DARK , rect = (95,90,100,100), text = get_icon_hex("play_arrow"), on_click= self.game_manager.start_round, positioning="relative"))
        self.items["lbl_round"].fore_color = (34,177,76)

        self.game_manager.change_level(self.no_turns,self.no_boxes,self.max_line_len)
        self.game_manager.entity_manager.add_entity(Player(self.game_manager,"player"), "player")
        self.btn_spawn_tower_on_click()
        self.toggle_dev()
    
    def draw(self):
        self.game_manager.draw(self.screen)
        super().draw()
    
    def update(self):
        super().update()
        self.game_manager.update()
        if pygame.key.get_just_pressed()[pygame.K_F5]:
            self.toggle_dev()
        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            self.pause()
        self.items["lbl_fps"].text = str(int(self.screen_manager.app.clock.get_fps()))
    
    def btn_back_on_click(self):
        self.game_manager.sound_manager.play_sound("click")
        self.screen_manager.change_screen(self.screen_manager.before_last_screen, 20)
    
    def btn_reload_on_click(self):
        self.assets.load()
        for group in self.game_manager.entity_manager.entities:
            for entity in self.game_manager.entity_manager.entities[group]:
                entity.sprite = pygame.transform.scale_by(self.assets.get(entity.__class__.__name__.lower()),2)
        
    def btn_generate_on_click(self):
        self.game_manager.sound_manager.play_sound("click")
        self.game_manager.change_level(self.no_turns, self.no_boxes, self.max_line_len)
        self.game_manager.entity_manager.remove_group("enemy")
    
    def btn_spawn_enemy_on_click(self):
        self.game_manager.sound_manager.play_sound("click")
        self.game_manager.level_manager.change_to_boss()
        self.game_manager.entity_manager.add_entity(Boss(self.game_manager, self.assets.get("boss")), "boss")
        
    def btn_spawn_tower_on_click(self):
        self.game_manager.sound_manager.play_sound("click")
        tower = Tower(self.game_manager, pygame.Vector2(SCREEN_WIDTH / 2, 0))
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

    def pause(self):
        if self.game_manager.time_paused == True and self.items.get("lbl_paused", None) != None:
            self.game_manager.time_paused = False
            self.remove_item("lbl_paused")
            self.remove_item("rect_pause")
            self.remove_item("btn_settings")
            self.remove_item("btn_continue")
            self.remove_item("btn_exit")
            self.items["btn_roundstart"].hidden = False
            return
        if self.game_manager.time_paused == True:
            return
        self.game_manager.level_manager.game_surf = pygame.transform.gaussian_blur(self.game_manager.level_manager.game_surf, 2)
        self.game_manager.time_paused = True
        self.add_item("rect_pause", Rect(RECT_DARK, (50, 50, 500, 500), positioning="relative"))
        self.add_item("lbl_paused", Label(LABEL_DARK, (50, 8, 1000, 100), text= "PAUSED", positioning="relative", font_size=80))
        self.add_item("btn_settings", Button(BUTTON_DARK, (50, 51, 400, 100), text="SETTINGS", on_click=self.screen_manager.change_screen, click_args=["settings", 1], positioning="relative"))
        self.add_item("btn_continue", Button(BUTTON_DARK, (50, 28, 400, 100), text="CONTINUE", on_click=self.pause, positioning="relative"))
        self.add_item("btn_exit", Button(BUTTON_DARK, (50, 73, 400, 100), text="EXIT", on_click=self.screen_manager.change_screen, click_args=["game_select", 1], positioning="relative"))
        self.items["btn_roundstart"].hidden = True
        
      

class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.assets = self.game.assets 
        self.level_manager = level.LevelManager(SCREEN_SCALE)
        self.entity_manager = entity.EntityManager()
        self.sound_manager = sound.SoundManager()
        self.screen_offset = pygame.Vector2(0,0)
        self.shake_duration = 0 
        self.shake_strength = 0 

        self.time_paused = False
        self.current_upgrade_choices = []

        self.round_started = False
        self.enemies = []
        self.spawn_counter = 0
        self.round = 0
        self.enemy_count = 0

        self.enemy_types = {
            "standard": {
                "type": Standard,
                "offset": 0
                },
            "fast": {
                "type": Fast,
                "offset": 2
                }
            }
        

    def update(self):

        self.level_manager.update()
        if not self.time_paused:
            self.entity_manager.update()
            if self.shake_duration > 0:
                dir = pygame.Vector2(0,self.shake_strength)
                dir = dir.rotate(random.randrange(360))
                self.screen_offset = dir
                self.shake_duration -= 1
            if self.shake_duration <= 0:
                self.shake_strength = 0 
                self.screen_offset = pygame.Vector2(0,0)
            if self.round_started:
                player = self.entity_manager.entities["player"][0]
                if self.spawn_counter % 75 == 0:
                    self.spawn_counter = 0 
                    if not len(self.enemies) == 0:
                        self.spawn_enemy(self.enemies[0])
                        self.enemies.pop(0)
                self.spawn_counter += 1
                if self.entity_manager.entities.get("enemy", []) == [] and self.enemy_count > 0:
                     self.round_started = False
                     self.give_upgrade()
            self.enemy_count = len(self.entity_manager.entities.get("enemy", []))
    
    def draw(self, screen):
        if not self.time_paused:
            self.level_manager.draw()
            self.entity_manager.draw(self.level_manager.game_surf)
        screen.blit(pygame.transform.scale(self.level_manager.game_surf,( SCREEN_WIDTH, SCREEN_HEIGHT)), self.screen_offset)
        
    def change_level(self, no_turns, no_boxes, max_line_len):
        for group in self.entity_manager.entities:
            for entity in self.entity_manager.entities[group]:
                entity.pos = pygame.Vector2(SCREEN_WIDTH/2,0)
                entity.velocity = pygame.Vector2(0,random.randrange(8,15))
                entity.velocity.rotate_ip(random.randrange(-45,45))
        self.level_manager.game_surf = pygame.transform.gaussian_blur(self.level_manager.game_surf, 2)
        self.level_manager.change_level(no_turns, no_boxes, max_line_len)

    def spawn_enemy(self, enemy):
        self.entity_manager.add_entity(enemy, "enemy")
    
    def give_upgrade(self):
        self.level_manager.game_surf = pygame.transform.gaussian_blur(self.level_manager.game_surf, 2)
        self.game.add_item("btn_upgrade_1", Button(BUTTON_DARK, (20,65,310,200), "speed", positioning="relative", on_click=self.spawn_upgrade, click_args=["speed"]))
        self.game.items["btn_upgrade_1"].fore_color = (34,177,76)
        self.game.add_item("btn_upgrade_2", Button(BUTTON_DARK, (50,65,430,200), "damage", positioning="relative", on_click=self.spawn_upgrade, click_args=["damage"]))
        self.game.items["btn_upgrade_2"].fore_color = (235,51,36)
        self.game.add_item("btn_upgrade_3", Button(BUTTON_DARK, (80,65,310,200), "range", positioning="relative", on_click=self.spawn_upgrade, click_args=["range"]))
        self.game.items["btn_upgrade_3"].fore_color = (230,230,230)
        self.game.add_item("lbl_upgrade", Label(LABEL_DARK_FILLED, (50,25,770,150), f"chose an upgrade", positioning="relative", font_size=80))
        self.time_paused = True    
        
    def show_upgrade_popup(self, tower):
        self.level_manager.game_surf = pygame.transform.gaussian_blur(self.level_manager.game_surf, 2)
        self.game.add_item("btn_cancel", Button(BUTTON_DARK, (25,65,450,200), "CANCEL", positioning="relative", on_click=self.cancel_on_click))
        currently_upgrading = None 
        for upgrade in self.entity_manager.entities["upgrade"]:
            if upgrade.can_upgrade:
                currently_upgrading = upgrade
        self.game.add_item("btn_upgrade", Button(BUTTON_DARK, (75,65,450,200), "UPGRADE", positioning="relative", on_click=self.upgrade_on_click, click_args=[currently_upgrading, tower]))
        self.game.add_item("lbl_upgrade", Label(LABEL_DARK_FILLED, (50,25,770,150), f"upgrade, {currently_upgrading.type}", positioning="relative", font_size=80))
        self.time_paused = True 

    def spawn_upgrade(self, upgrade_type):
        self.shake_screen(10, 10)
        self.game.remove_item("btn_upgrade_1")
        self.game.remove_item("btn_upgrade_2")
        self.game.remove_item("btn_upgrade_3")
        self.game.remove_item("lbl_upgrade")
        upgrade = Upgrade(self, pygame.Vector2(SCREEN_WIDTH / 2, 0), self.assets.get(f"{upgrade_type}_upgrade"), upgrade_type)
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

    def start_round(self):
        if not self.round_started and self.entity_manager.entities.get("boss", []) != []:  
            no_enemies = len(self.enemies)
            self.enemy_count = len(self.entity_manager.entities.get("enemy", []))
            if no_enemies > 0 and self.enemy_count == 0:
                self.round_started = True
            return
        if self.round_started or self.entity_manager.entities.get("enemy", []) != []: return
        self.round += 1
        self.game.items["lbl_round"].text = str(self.round)
        self.round_started = True
        for type in self.enemy_types:
            number = -(2.5 - (self.round - self.enemy_types[type]["offset"]))**2 + 10
            number //= 2 
            number = math.tanh((self.round - self.enemy_types[type]["offset"])/ 3)
            number = (number * 4)
            if self.round >= self.enemy_types[type]["offset"]:
                number = math.sqrt((self.round - self.enemy_types[type]["offset"]) * 6)
            if number > 0:
                for i in range(int(number)):
                    self.enemies.append(self.enemy_types[type]["type"](self, sprite = self.assets.get("enemy1")))