import pygame
import sys
import os 

from game.level import Generator
from .sound import SoundManager
from .entity import EntityManager
from .screen_manager import *
from .screen import Screen
from screens import *
from .ui import *

from entities.player import Player

screens = {
    "menu": Menu,
    "game_select": Game_select, 
    "settings": Settings,
    "heroes": Heroes,
    "upgrades": Upgrades
    }

class Assets: 
    def __init__(self) -> None:
        self.assets = {}
        self.load()
    
    def load(self):
        for file in os.scandir("assets/images"):
            if file.is_dir():
                for file in os.scandir(file.path):
                    if file.name.split(".")[-1] == "png":
                        self.assets[file.name.split(".")[0]] = pygame.image.load(file.path)
                        self.assets[file.name.split(".")[0]].set_colorkey((0,0,0))
            if file.name.split(".")[-1] == "png":
                self.assets[file.name.split(".")[0]] = pygame.image.load(file.path)
                self.assets[file.name.split(".")[0]].set_colorkey((0,0,0))

    def get(self, key):
        return self.assets.get(key, self.assets["null"])


class Engine:
    def __init__(self, screens):
        self.config = self.load_config()
        self.running = True
        
        # setup the display
        self.screen = pygame.display.set_mode((int(self.config.get("SCREEN_WIDTH")), int(self.config.get("SCREEN_HEIGHT"))))

        # get all the managers in one place finally thank god
        self.screen_manager = ScreenManager("menu", screens)
        self.sound_manager = SoundManager()
        self.entity_manager = EntityManager()

        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            self.check_events()
            self.draw()
            self.update()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
                self.running = False

    def update(self):
        self.screen_manager.update()

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen_manager.draw()
        pygame.display.flip()
        
        
    def load_config(self):
        config = {}
        with open("config.cfg") as fconfig:
            for line in fconfig.readlines():
                if line[0] != "#" and len(line.split(" ")) > 1:
                    config[line.split(" ")[0]] = line.split(" ")[1]
        return config

class Game(Engine):
    def __init__(self):
        super().__init__(screens)
        # holds whether or not the game screen is open
        self.game_active = False

        # setup game screen
        self.game_screen = Screen(self.screen_manager)
        self.screen_manager.add_screen("game", self.game_screen)

        # level data / generation
        self.level_data = {
            "no_turns": 6,
            "no_boxes": 6,
            "max_line_len": 1000
            }
        self.generator = Generator(self.screen.get_size())
        self.level = self.generator.generate_level(self.level_data)
        
        # setup draw and update queues
        self.draw_queue = {1:[],2:[],3:[],4:[],5:[],6:[]}
        self.update_queue = []

        # assets
        self.assets = Assets()

        self.draw_queue[1].append(self.level)
        self.draw_queue[2].append(self.entity_manager)
        self.update_queue.append(self.entity_manager)

        self.entity_manager.add_entity(Player(self,"player"),"player")

    def draw(self):
        if self.game_active:
            layers = sorted(self.draw_queue.keys())
            for layer in layers:
                for item in self.draw_queue[layer]:
                    item.draw()
            pygame.display.flip()
        else:
            super().draw()

    def update(self):
        self.game_active = self.screen_manager.current_screen == "game"
        if self.game_active:
            for item in self.update_queue:
                item.update()
        else:
            super().update()