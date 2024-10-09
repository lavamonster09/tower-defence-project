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

from entities import *

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
        self.config, self.keybinds = self.load_config()
        self.running = True
        
        # setup the display
        self.screen = pygame.display.set_mode((int(self.config.get("SCREEN_WIDTH")), int(self.config.get("SCREEN_HEIGHT"))))

        # get all the managers in one place finally thank god
        self.sound_manager = SoundManager(self)
        self.entity_manager = EntityManager()
        self.screen_manager = ScreenManager(self, "menu", screens)
        
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
        keybinds = {}
        with open("config.cfg") as fconfig:
            for line in fconfig.readlines():
                split = line.split(" ")
                if line[0] != "#" and len(split) > 1:
                    if split[0].upper() == "BIND":
                        keybinds[split[2].strip("\n")] = pygame.key.key_code(split[1])
                        continue
                    config[split[0]] = split[1].strip("\n")
        return config, keybinds
    